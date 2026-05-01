# Spec: Login and Logout

## Overview
This step wires up session-based authentication for Spendly. Users who registered in Step 2 can now log in with their email and password; a successful login stores their `user_id` in the Flask session and redirects them to their profile. Logging out clears the session and returns them to the landing page. This is the gateway step — every protected route in later steps depends on a populated session.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (`create_user()`, password hashed with werkzeug)

## Routes
- `POST /login` — validate credentials, set session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/` — public (safe to call even if not logged in)

## Database changes
No database changes. The `users` table already has `email` and `password_hash` columns sufficient for login.

## Templates
- **Modify:** `templates/login.html` — add `method="POST"` and `action="{{ url_for('login') }}"` to the form; add named `email` and `password` inputs; render flashed messages
- **Modify:** `templates/base.html` — update nav links to show a "Logout" link when `session.user_id` is set, and "Login" / "Register" links when it is not

## Files to change
- `app.py` — add `POST /login` handler; implement `GET /logout`; import `check_password_hash` from `werkzeug.security` (or rely on db helper); import `session` from Flask
- `templates/login.html` — form wiring and flash message display
- `templates/base.html` — session-aware nav

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` is already available via Flask.

## Rules for implementation
- No SQLAlchemy or ORMs — raw sqlite3 via `get_db()` only
- Parameterised queries only (`?` placeholders) — never f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values in any template or stylesheet
- All templates extend `base.html`
- Session key must be `user_id` (integer) — no other shape
- On failed login, flash a generic message ("Invalid email or password") — never reveal which field was wrong
- `GET /logout` must call `session.clear()`, not `session.pop('user_id')`, to wipe the full session
- After successful login, redirect to `url_for('profile')` using `redirect()`
- After logout, redirect to `url_for('index')` using `redirect()`
- Add a helper `get_user_by_email(email)` in `database/db.py` — do not put the SELECT query inline in the route

## Definition of done
- [ ] Visiting `/login` renders the login form with email and password fields
- [ ] Submitting the form with a valid registered email and correct password redirects to `/profile`
- [ ] After login, `session['user_id']` matches the user's `id` in the database
- [ ] Submitting the form with a valid email but wrong password stays on `/login` and shows a flash error
- [ ] Submitting the form with an unregistered email shows the same generic flash error
- [ ] Visiting `/logout` clears the session and redirects to the landing page `/`
- [ ] After logout, visiting `/logout` again redirects to `/` without error
- [ ] The nav in `base.html` shows "Login" and "Register" when logged out, and "Logout" when logged in
- [ ] The seeded demo user (`demo@spendly.com` / `demo1234`) can log in successfully
