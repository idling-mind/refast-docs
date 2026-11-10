# Advanced Section — Agent Instructions

## Section Goal

Deep-dive topics for **framework extenders and advanced users**. These pages should be
thorough technical references adapted from the existing `.md` docs in the `docs/` folder.

---

## Pages

### 1. `component_dev.py` — Building Components (`/docs/advanced/component-dev`)

**Adapt from:** `docs/COMPONENT_DEVELOPMENT.md` (1938 lines), `docs/NAMING_CONVENTIONS.md`

**Cover:**
- **Architecture overview** — Python class + React component + ComponentRegistry
- **Python side**: Subclass `Component`, implement `render()`, define `component_type`
- **Common props**: id, class_name, children, style, callbacks
- **Children rendering**: `self._render_children()`
- **React side**: Create functional component, register in `ComponentRegistry`
- **Naming conventions**: `snake_case` (Python) → `camelCase` (JSON/React) automatic conversion
- **Callback props**: How `on_click` etc. are serialized and handled
- **Step-by-step walkthrough**: Create a complete custom component from scratch
- **Testing**: How to test custom components

---

### 2. `extension_dev.py` — Building Extensions (`/docs/advanced/extension-dev`)

**Adapt from:** `docs/EXTENSION_DEVELOPMENT.md` (1247 lines)

**Cover:**
- **Extension class**: Subclass `Extension`, define name/version/scripts/styles
- **Project structure**: Python package + static assets
- **Static path**: `@property static_path -> Path`
- **Components**: `@property components -> list` — Python component classes
- **Frontend bundle**: UMD module format, `window.RefastExtensions` / `window.RefastComponentRegistry`
- **Entry points**: `[project.entry-points."refast.extensions"]` in pyproject.toml
- **Auto-discovery**: `auto_discover_extensions=True` on RefastApp
- **Asset serving**: `/static/ext/{name}/{file}` URL pattern
- **on_register()**: Called when extension is registered with app
- **validate()**: Checks static_path exists
- **Building**: How to build the UMD bundle (vite/rollup/webpack)
- **Publishing**: PyPI distribution with entry points
- **Complete example**: Walk through a full extension implementation

---

### 3. `security.py` — Security (`/docs/advanced/security`)

**Read:** All files in `src/refast/security/`

**Cover:**
- **SecurityMiddleware**: Combined middleware (constructor params, processing order)
- **CSRF Protection**: Double-submit cookie, HMAC-SHA256, generate/validate tokens
- **Rate Limiter**: Sliding window, per-key tracking, max_requests/window_seconds
- **Input Sanitizer**: Script tag removal, event handler stripping, javascript: URL blocking
- **Content Security Policy**: CSP header construction, `for_refast()` preset, `for_development()`
- **Configuration examples**: Production vs development setups
- **Decorator usage**: `@csrf_required`, `@rate_limit`, `@sanitize_input`

---

### 4. `sessions.py` — Sessions (`/docs/advanced/sessions`)

**Read:** All files in `src/refast/session/`

**Cover:**
- **Session class**: Dict-like interface, `get`/`set`/`delete`, bracket syntax, `clear`,
  `destroy`, `set_expiry(seconds)`, `save`, `is_modified`, `id`
- **SessionData**: `id`, `data`, `created_at`, `updated_at`, `expires_at`
- **MemorySessionStore**: In-memory dict (`default_ttl`, `cleanup_interval`); per-process,
  so it does not work across workers
- **RedisSessionStore**: Redis-backed (`redis_url` or an existing `client`, `prefix`,
  `default_ttl`)
- **SessionMiddleware**: `store`, `cookie_name`, `cookie_max_age`, `cookie_path`,
  `cookie_domain`, `cookie_secure`, `cookie_httponly`, `cookie_samesite`, `secret_key`
- **get_session dependency**: FastAPI dependency injection
- **State vs Session vs Store comparison table** (lifetime, persistence, sharing)
- **Production recommendations**: Redis store, `cookie_secure=True`, TTL settings

**Traps that have already been documented wrongly once — check before writing:**

- The store classes are `MemorySessionStore` / `RedisSessionStore`; `MemoryStore` and
  `RedisStore` do not exist, and they are exported from `refast.session`.
- The middleware parameter is `cookie_max_age`, not `max_age`.
- `SessionMiddleware` subclasses `BaseHTTPMiddleware`, so WebSocket connections never
  reach it. `ctx.session` is built by `Context` with no store, which makes it
  per-connection unless the middleware attached one to `request.state.session`. Do not
  describe `ctx.session` as surviving a reload.
- `secret_key` is stored but unused — its docstring says signing is future work. The
  cookie carries an opaque id, not signed data.
- `ctx.store.session` is the browser's `sessionStorage`, a different mechanism entirely.

---

### 5. `../concepts/styling.py` — Styling (`/docs/concepts/styling`)

> Note: this page lives in the **Core Concepts** section (`docs/pages/concepts/styling.py`),
> not in `docs/pages/advanced/`.

**Adapt from:** `docs/STYLING_GUIDE.md`, `docs/TAILWIND_SUPPORT.md`

**Cover:**
- **class_name prop**: How every component accepts Tailwind classes
- **Semantic color tokens**: Complete list (background, foreground, primary, secondary, muted, accent, destructive, card, popover, border, input, ring, sidebar, chart-1 through chart-5)
- **Available Tailwind classes**: Layout, spacing (0-6, 8, 10, 12, 16), typography, colors, borders, responsive breakpoints
- **Responsive design**: `sm:`, `md:`, `lg:`, `xl:` prefixes
- **style prop**: When to use it (dynamic values only), examples
- **Custom CSS**: `ui.add_css()`, `custom_css` parameter
- **Custom JS**: `ui.add_js()`, `custom_js` parameter
- **Head tags**: `ui.add_head_tag()` — meta tags, fonts, etc.
- **What's NOT included**: Full Tailwind — only the bundled subset
