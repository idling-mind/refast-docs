"""Sessions — /docs/advanced/sessions."""

from refast.components import Alert, Container, Heading, Markdown, Separator

PAGE_TITLE = "Sessions"
PAGE_ROUTE = "/docs/advanced/sessions"


def warning_comp(message: str):
    return Alert(
        title="Careful",
        message=message,
        variant="warning",
    )


def render(ctx):
    """Render the sessions guide page."""
    from docs.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT, custom_tags={"Warning": warning_comp}),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
## Overview

A *session* is the record of who is making a request, carried between requests by
a cookie. Refast ships a small server-side session layer — a `Session` object, a
pluggable store behind it, and middleware that joins the two — for the cases where
data should outlive the tab that created it.

<Warning>
Three unrelated things in Refast carry the word "session": `ctx.session` (the
server-side object on this page), `ctx.store.session` (the browser's
`sessionStorage`, see [State Management](/docs/concepts/state)), and the session
id in the `refast_session` cookie. Only the first is server-side state.
</Warning>

## `ctx.session`

`ctx.session` is a `refast.session.Session`: a dict-like bag of values with an id.

```python
from refast import Context

def profile(ctx: Context):
    ctx.session.set("theme", "dark")     # Session.set(key, value)
    theme = ctx.session.get("theme")     # Session.get(key, default=None)
    del ctx.session["theme"]             # __delitem__ is implemented
```

| Method | Signature | Notes |
|---|---|---|
| `get` | `get(key, default=None)` | Read a value. |
| `set` | `set(key, value)` | Write a value and mark the session modified. |
| `delete` | `delete(key)` | Remove one key. |
| `clear` | `clear()` | Empty every key, keep the session. |
| `destroy` | `destroy()` | Delete from the store and empty the data. |
| `save` | `await save()` | Write through to the store if modified. |
| `set_expiry` | `set_expiry(seconds)` | Absolute lifetime from now. |
| `keys` / `values` / `items` | — | Iteration over the stored mapping. |
| `to_dict` | `to_dict()` | Plain dict, including timestamps. |
| `is_modified` / `is_expired` | — | Flags used by the middleware. |
| `id` / `session_id` | — | The value that goes in the cookie. |

Bracket access works as well as the methods: `session["role"] = "admin"` is
equivalent to `session.set("role", "admin")`, and `in` tests membership.

### What it is *not* persisted by

`Context.session` builds the object on first access:

```python
@property
def session(self) -> "Session":
    if self._session is None:
        self._session = Session()      # no store
    return self._session
```

No store, so `save()` has nothing to write to: values live on that one `Context`
object. On a page load the context is created for the HTTP request and thrown
away with it; on a live WebSocket connection it survives as long as the
connection does. Writing to `ctx.session` inside a callback is therefore no more
durable than writing to `ctx.state` — the persistence below is what changes that.

## Making it durable

`refast.session.SessionMiddleware` resolves the session for each HTTP request: it
reads the cookie, loads the matching entry from the store (or starts a new
session), attaches it to the request, and saves it back when the response is
produced.

```python
from fastapi import FastAPI
from refast import RefastApp
from refast.session import MemorySessionStore, SessionMiddleware

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    store=MemorySessionStore(default_ttl=3600),
    cookie_name="refast_session",
    cookie_max_age=3600,
    cookie_httponly=True,
    cookie_samesite="lax",
)

ui = RefastApp(title="My App")
app.include_router(ui.router)
```

| Parameter | Default | Purpose |
|---|---|---|
| `store` | `None` | A `SessionStore`; without one the middleware still mints ids but nothing is written. |
| `cookie_name` | `"refast_session"` | Cookie key holding the session id. |
| `cookie_max_age` | `3600` | Cookie lifetime in seconds. Note the `cookie_` prefix. |
| `cookie_path` | `"/"` | Cookie path. |
| `cookie_domain` | `None` | Cookie domain. |
| `cookie_secure` | `False` | Send only over HTTPS. Set this to `True` in production. |
| `cookie_httponly` | `True` | Hide the cookie from JavaScript. |
| `cookie_samesite` | `"lax"` | CSRF posture of the cookie. |
| `secret_key` | `None` | Accepted and stored, but not used for anything yet — the middleware docstring marks signing as future work. The cookie holds an opaque id, so this is not a signed-cookie scheme. |

The middleware is a `BaseHTTPMiddleware`, so it sees HTTP requests only: page
loads and REST routes. **WebSocket upgrades do not pass through it**, which means
`ctx.session` inside a callback is still the unstored object described above.
Inside a page function the request is available, so the session the middleware
built is reachable through it:

```python
def dashboard(ctx: Context):
    request = ctx.request
    session = request.state.session if request else None
    user_id = session.get("user_id") if session else None
```

In a plain route, prefer the dependency, which returns the same object:

```python
from refast.session import get_session

@app.get("/api/whoami")
async def whoami(session=Depends(get_session)):
    return {"user_id": session.get("user_id"), "session_id": session.id}
```

## Stores

The store is the durable half. Both built-ins satisfy the `SessionStore`
interface — `set`, `get`, `delete`, `exists`, `touch`, `clear_expired` — so
swapping one for the other changes nothing else.

### `MemorySessionStore`

```python
from refast.session import MemorySessionStore

store = MemorySessionStore(default_ttl=3600, cleanup_interval=300)
```

A process-local dict with expiry sweeping. Nothing survives a restart, and
multiple workers do not share it: a session created by worker A is unknown to
worker B, so the cookie will look like a logged-out user half the time.

### `RedisSessionStore`

```python
from refast.session import RedisSessionStore

store = RedisSessionStore(
    redis_url="redis://localhost:6379",
    prefix="refast:session:",
    default_ttl=3600,
)
```

Pass either `redis_url` (the store creates its client) or an existing `client`.
Keys are namespaced with `prefix`, and the TTL is refreshed by `touch` on read.

## Choosing somewhere to put a value

| | `ctx.state` | `ctx.session` | `ctx.store.local` | `ctx.store.session` | Cookie |
|---|---|---|---|---|---|
| Lives in | Server, on the `Context` | Server store, keyed by id | Browser `localStorage` | Browser `sessionStorage` | Browser, sent on every request |
| Survives reload | No | Yes | Yes | Yes | Yes |
| Survives closing the tab | No | Yes (until TTL) | Yes | No | Per `max_age` |
| Visible to other tabs | No | Same store, different context | Yes | No | Yes |
| Readable in a page function | Yes | Yes | Through the browser only | Through the browser only | `ctx.request.cookies` |
| Needs setup | No | Middleware plus a store | No | No | No |

The usual login flow puts an id in the session and nothing else: the session
cookie then authenticates the visitor, while the profile itself comes from the
database.

## Next Steps

- [Security](/docs/advanced/security) — Cookie flags, CSRF, and rate limiting
- [State Management](/docs/concepts/state) — `ctx.state` and the browser stores
- [File Transfers](/docs/concepts/file-transfers) — `ui.file_store`, the other
  server-side store
"""
