"""Security — /docs/advanced/security."""
from typing import Any, Literal

from refast.components import Container, Heading, Markdown, Separator, Alert

PAGE_TITLE = "Security"
PAGE_ROUTE = "/docs/advanced/security"

def warning_comp(message: str):
    return Alert(
        title="Warning",
        message=message,
        variant="warning",
    )


def render(ctx):
    """Render the security guide page."""
    from docs.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT, custom_tags={"Warning": warning_comp}),
            # Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
## Overview

Security is a core design principle of Refast. The framework provides built-in mechanisms to safeguard your applications against common web vulnerabilities, including Cross-Site Request Forgery (CSRF), rate-limiting abuse, Cross-Site Scripting (XSS), and clickjacking/MIME-sniffing exploits.

You can configure and enable security features individually, or apply them globally across your entire app using `SecurityMiddleware`.

---

## SecurityMiddleware

`SecurityMiddleware` is an all-in-one ASGI middleware that integrates all Refast security features. By attaching it to your FastAPI instance, you get automated protection with minimal setup.

### Order of Operations
When a request enters the server, `SecurityMiddleware` processes it in this order:
1. **Rate Limit Check**: Evaluates if the client has exceeded their request quota. If exceeded, blocks the request immediately with an HTTP 429 status.
2. **Request Dispatch**: Forwards the request down the middleware chain to be processed by your page handlers or APIs.
3. **Response Headers**: Appends standard HTTP security headers (CSP, HSTS, X-Frame-Options, etc.).
4. **CSRF Token Generation**: Automatically generates a secure CSRF token and sets it as a client-readable cookie on all incoming `GET` requests.

### Configuration Parameters
- `secret_key` (`str`): The key used to sign CSRF tokens and cookies. Keep this key secure.
- `csrf_enabled` (`bool`): Toggle CSRF protection (default: `True`).
- `csrf_config` (`CSRFConfig` | `None`): Detailed configuration settings for CSRF.
- `rate_limit_enabled` (`bool`): Toggle global rate limiting (default: `True`).
- `rate_limit` (`int`): Maximum requests allowed per window (default: `100`).
- `rate_limit_window` (`int`): Sliding window size in seconds (default: `60`).
- `csp` (`ContentSecurityPolicy` | `None`): Content Security Policy configuration. Defaults to `ContentSecurityPolicy.for_refast()`.
- `hsts_enabled` (`bool`): Enable HTTP Strict Transport Security (default: `True`).
- `hsts_max_age` (`int`): HSTS expiration in seconds (default: 31,536,000 / 1 year).
- `x_content_type_options` (`bool`): Prevent MIME-type sniffing (default: `True`).
- `x_frame_options` (`str`): X-Frame-Options value to block framing (default: `"DENY"`).
- `x_xss_protection` (`bool`): Legacy script blocking (default: `True`).

### Complete Example Application

Below is a complete sample Refast app showing how to conditionally set up `SecurityMiddleware` for both production and development environments:

```python
import os
from fastapi import FastAPI
import uvicorn
from refast import RefastApp, Context
from refast.components import Column, Heading, Text
from refast.security import SecurityMiddleware, ContentSecurityPolicy, CSRFConfig

# 1. Initialize FastAPI app
app = FastAPI()

# Determine current environment
IS_PRODUCTION = os.getenv("ENV") == "production"

# 2. Configure Content Security Policy
if IS_PRODUCTION:
    # Strict policy for production
    csp = ContentSecurityPolicy(
        default_src=["'self'"],
        script_src=["'self'"],  # Blocks inline scripts in production
        style_src=["'self'", "'unsafe-inline'"],
        img_src=["'self'", "data:", "https://trusted-assets.com"],
        connect_src=["'self'", "wss:"],  # Restricts WebSocket connections to SSL
        frame_ancestors=["'none'"],      # Blocks iframe clickjacking
        upgrade_insecure_requests=True   # Directs browser to upgrade HTTP to HTTPS
    )
else:
    # Permissive configuration for development (supports hot-reloading)
    csp = ContentSecurityPolicy.permissive()

# 3. Add SecurityMiddleware to FastAPI
app.add_middleware(
    SecurityMiddleware,
    secret_key=os.getenv("SECRET_KEY", "dev-secure-key-32-chars-at-least"),
    csrf_enabled=True,
    csrf_config=CSRFConfig(
        cookie_name="csrf_token",
        cookie_secure=IS_PRODUCTION,   # Require HTTPS in production
        cookie_httponly=False,         # Must be False for JS to access the token
        token_expiry=3600,             # 1 hour lifespan
    ),
    rate_limit_enabled=True,
    rate_limit=100,                    # Allow 100 requests
    rate_limit_window=60,              # Per 60 seconds
    csp=csp,
    hsts_enabled=IS_PRODUCTION,
)

# 4. Initialize RefastApp
ui = RefastApp(title="Secured App")

@ui.page("/")
def home(ctx: Context):
    return Column(
        class_name="p-8 h-screen",
        align="center",
        justify="center",
        children=[
            Heading("Secured App"),
            Text("This app is fully protected by Refast's global SecurityMiddleware.")
        ]
    )

app.include_router(ui.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

## CSRF Protection

Refast protects mutable endpoints (e.g., `POST`, `PUT`, `DELETE` operations) from Cross-Site Request Forgery via the **Double-Submit Cookie Pattern** with HMAC-SHA256 signature verification.

While standard Refast WebSocket connections are scoped to the connection and session lifetime, file uploads via the `FileUploader` component send files via HTTP `POST` requests. `SecurityMiddleware` automatically validates these requests using a CSRF token. The frontend client reads the `csrf_token` cookie and automatically appends it to the `X-CSRF-Token` header.

### Complete Example Application

The sample app below illustrates enabling CSRF protection globally and processing files uploaded securely using the Refast `FileUploader` component:

```python
from fastapi import FastAPI
import uvicorn
from refast import RefastApp, Context
from refast.components import Column, Heading, FileUploader, Text
from refast.security import SecurityMiddleware, CSRFConfig

# 1. Initialize FastAPI app
app = FastAPI()

# 2. Add SecurityMiddleware to enforce CSRF on all POST endpoints (including /api/upload)
app.add_middleware(
    SecurityMiddleware,
    secret_key="my-secret-key-change-in-production",
    csrf_enabled=True,
    csrf_config=CSRFConfig(
        cookie_name="csrf_token",
        cookie_secure=False,  # Set True in production
        token_expiry=3600     # 1 hour expiration
    ),
    rate_limit_enabled=False
)

# 3. Initialize RefastApp
ui = RefastApp(title="Secure Upload App")

async def handle_upload_complete(ctx: Context, files: list[dict]):
    # Callback triggered after frontend successfully uploads the files.
    # The client-side FileUploader component read the CSRF cookie and
    # sent the X-CSRF-Token header to pass validation.
    for f in files:
        file_id = f["id"]
        filename = f["name"]
        content = await ctx.app.file_store.get_file(file_id)
        # Process data securely here...
        
    await ctx.show_toast(f"Uploaded {len(files)} files securely!", variant="success")

@ui.page("/")
def upload_page(ctx: Context):
    return Column(
        class_name="p-8 max-w-md mx-auto",
        children=[
            Heading("Secure File Upload", level=2),
            FileUploader(
                label="Select or drag files here",
                multiple=True,
                on_upload_complete=ctx.callback(handle_upload_complete)
            )
        ]
    )

app.include_router(ui.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

## Rate Limiting

Abuse and denial-of-service attempts are mitigated by an in-memory, thread-safe **Sliding Window** rate limiter.

In Refast, page requests are HTTP GET requests and are automatically rate-limited by `SecurityMiddleware`. However, if you want to conditionally restrict access inside your page function or custom route, you can call `is_allowed()` manually on a `RateLimiter` instance.

### Complete Example Application

Below is an application showing how to implement manual rate-limiting inside a Refast page function:

```python
from fastapi import FastAPI, HTTPException
import uvicorn
from refast import RefastApp, Context
from refast.components import Column, Heading, Text
from refast.security import RateLimiter

app = FastAPI()

# 1. Initialize rate limiter (Max 5 requests per 30 seconds)
limiter = RateLimiter(max_requests=5, window_seconds=30)

ui = RefastApp(title="Rate Limited Refast App")

@ui.page("/")
async def home(ctx: Context):
    # During page functions, ctx.request is populated with the Starlette Request
    if ctx.request:
        allowed, info = await limiter.is_allowed(ctx.request)
        if not allowed:
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded. Try again in {info['reset']} seconds."
            )
            
    return Column(
        class_name="p-8 h-screen",
        align="center",
        justify="center",
        children=[
            Heading("Rate Limited Page"),
            Text("Welcome! If you reload this page too many times, you will be rate-limited.")
        ]
    )

app.include_router(ui.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

## Input Sanitization

Refast handles XSS prevention by cleaning user inputs. The `InputSanitizer` scans strings to strip dangerous elements.

In Refast page callbacks, user input data is transmitted via `ctx.event_data` (e.g. from forms). You can use `InputSanitizer` to sanitize these values before saving them or updating state.

### Complete Example Application

The application below illustrates how to validate schemas with `InputSanitizer.validate` inside a Refast form submission callback:

```python
from fastapi import FastAPI
import uvicorn
from refast import RefastApp, Context
from refast.components import Column, Heading, Form, Input, Button, Text
from refast.security import InputSanitizer

app = FastAPI()
ui = RefastApp(title="Sanitized Profile App")

sanitizer = InputSanitizer()

# Define validation schema
PROFILE_SCHEMA = {
    "display_name": {
        "type": "string",
        "required": True,
        "max_length": 50,
        "sanitize_html": True  # Strips HTML tags and script elements
    },
    "bio": {
        "type": "string",
        "max_length": 200,
        "sanitize_html": True
    }
}

async def handle_submit(ctx: Context):
    # Validate event data from form inputs against the schema
    try:
        clean_data = InputSanitizer.validate(ctx.event_data, PROFILE_SCHEMA)
    except ValueError as err:
        await ctx.show_toast(f"Validation Error: {err}", variant="destructive")
        return

    # Update state with cleaned/sanitized data
    ctx.state["display_name"] = clean_data["display_name"]
    ctx.state["bio"] = clean_data["bio"]
    
    await ctx.show_toast("Profile updated securely!", variant="success")
    await ctx.refresh()

@ui.page("/")
def profile_page(ctx: Context):
    name = ctx.state.get("display_name", "Anonymous User")
    bio = ctx.state.get("bio", "No bio provided yet.")
    
    return Column(
        class_name="p-8 max-w-md mx-auto",
        children=[
            Heading("User Profile"),
            Text(f"Name: {name}", class_name="font-semibold"),
            Text(f"Bio: {bio}", class_name="text-muted-foreground mb-4"),
            Form(
                on_submit=ctx.callback(handle_submit),
                children=[
                    Input(name="display_name", placeholder="Display Name", type="text", class_name="mb-2"),
                    Input(name="bio", placeholder="Bio", type="text"),
                    Button("Save Profile", type="submit", class_name="mt-4")
                ]
            )
        ]
    )

app.include_router(ui.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

## Content Security Policy (CSP)

A Content Security Policy (CSP) restricts resource loading (scripts, stylesheets, images, connections) to trustworthy sources to prevent code injection.

In Refast, CSP is applied globally via the `SecurityMiddleware`. If your app loads external assets (such as images from a CDN or external API scripts), you should customize the default policy and supply it to the middleware.

### Complete Example Application

Below is a complete Refast app showing how to customize and register a Content Security Policy for your Refast pages:

```python
import os
from fastapi import FastAPI
import uvicorn
from refast import RefastApp, Context
from refast.components import Column, Heading, Text
from refast.security import SecurityMiddleware, ContentSecurityPolicy

app = FastAPI()

# 1. Customize the standard Refast CSP policy
custom_csp = ContentSecurityPolicy.for_refast()

# Allow loading user avatars from a trusted external domain
custom_csp.img_src.append("https://images.unsplash.com")

# 2. Add SecurityMiddleware with custom CSP
app.add_middleware(
    SecurityMiddleware,
    secret_key="my-secret-key-change-in-production",
    csp=custom_csp,
    csrf_enabled=False,
    rate_limit_enabled=False
)

ui = RefastApp(title="CSP Protected Refast App")

@ui.page("/")
def home(ctx: Context):
    return Column(
        class_name="p-8",
        children=[
            Heading("CSP Configured"),
            Text("This page restricts loading images to self-origin and images.unsplash.com.")
        ]
    )

app.include_router(ui.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

## Callback Security & Input Validation

WebSockets callbacks mapped to `Context` (`ctx.callback(...)`) operate over public WebSocket frames. While callback mappings use random UUIDs and connection scoping to prevent cross-user execution, attackers can still capture, view, and falsify WebSocket payloads.

<Warning>
Bound callback parameters (`bound_args`) and event payload metadata (`props`) are visible and client-modifiable. Treat them as untrusted input.
</Warning>

### Guidelines for Callback Security

#### A. Perform Access Control (Authorization)
Always verify that the user's authenticated session identifier is authorized to mutate or access the resources specified in the callback arguments. Do not assume ownership based solely on parameters.

```python
async def delete_item(ctx: Context, item_id: int):
    # 1. Retrieve user identifier from the server-controlled session
    user_id = ctx.session.get("user_id")
    if not user_id:
        await ctx.show_toast("Authentication required", variant="destructive")
        return
    
    # 2. Check resource ownership in the database
    item = await db.get_item(item_id)
    if not item or item.owner_id != user_id:
        await ctx.show_toast("Access denied", variant="destructive")
        return
    
    # 3. Authorized
    await db.delete_item(item_id)
```

#### B. Validate event data with Pydantic
Validate payloads inside form handlers (available in `ctx.event_data`) using Pydantic models.

```python
from pydantic import BaseModel, EmailStr, constr, ValidationError

class MessageForm(BaseModel):
    recipient_email: EmailStr
    body: constr(min_length=1, max_length=500)

async def send_message(ctx: Context):
    try:
        # Validate structure and formats
        form = MessageForm(**ctx.event_data)
    except ValidationError as err:
        errors = {e["loc"][0]: e["msg"] for e in err.errors()}
        ctx.state["form_errors"] = errors
        await ctx.refresh()
        return

    await email_service.send(form.recipient_email, form.body)
```

#### C. Validate parameter types explicitly
Always assert parameter types in your callbacks. Check boundaries and convert variable inputs safely.

```python
async def select_page(ctx: Context, page_num: Any):
    try:
        page = int(page_num)
        if page < 1:
            raise ValueError
    except (ValueError, TypeError):
        await ctx.show_toast("Invalid page parameter", variant="destructive")
        return
        
    ctx.state["current_page"] = page
    await ctx.refresh()
```

### Complete Callback Security Example

Below is a complete Refast page showing callback verification, session lookup, Pydantic parsing, and input sanitization:

```python
from pydantic import BaseModel, constr, ValidationError
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Column, Heading, Form, Input, Button, Text
from refast.security import InputSanitizer

class BioUpdateModel(BaseModel):
    bio_text: constr(min_length=5, max_length=100)

# Callback target
async def update_bio_callback(ctx: Context, target_user_id: int):
    # 1. Authorization: Fetch current user from secure session
    logged_user_id = ctx.session.get("user_id")
    if not logged_user_id:
        await ctx.show_toast("You must be logged in.", variant="destructive")
        return

    # 2. Prevent Parameter Tampering / IDOR: Ensure the user is updating their own bio
    if logged_user_id != target_user_id:
        await ctx.show_toast("Security Alert: Unauthorized ID modification.", variant="destructive")
        return

    # 3. Input Validation via Pydantic
    try:
        form = BioUpdateModel(bio_text=ctx.event_data.get("bio", ""))
    except ValidationError as err:
        msg = err.errors()[0]["msg"]
        await ctx.show_toast(f"Input Error: {msg}", variant="destructive")
        return

    # 4. Input Sanitization
    sanitizer = InputSanitizer()
    clean_bio = sanitizer.sanitize(form.bio_text)

    # 5. Save safe data to Database
    await db.save_bio(logged_user_id, clean_bio)
    await ctx.show_toast("Bio updated successfully!", variant="success")
    await ctx.refresh()

# Page render
ui = RefastApp(title="Profile App")

@ui.page("/profile")
def profile_page(ctx: Context):
    # Fetch active user from session (mocking user_id=42 for demonstration)
    user_id = ctx.session.get("user_id", 42)
    
    return Column(
        class_name="p-8 max-w-md mx-auto",
        children=[
            Heading("Edit Profile Bio"),
            Form(
                # target_user_id is passed as a bound arg. It will be verified in callback.
                on_submit=ctx.callback(update_bio_callback, target_user_id=user_id),
                children=[
                    Input(name="bio", placeholder="Tell us about yourself...", type="text"),
                    Button("Save", type="submit", class_name="mt-4")
                ]
            )
        ]
    )
```

---

## Next Steps

- [Sessions](/docs/advanced/sessions) — Secure server-side session stores
- [Styling](/docs/concepts/styling) — Designing layout and themes
"""
