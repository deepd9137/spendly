# Spec: Registration

## Overview
This step wires up the registration form so new users can create a Spendly account. The `GET /register` route already renders the template stub; this step adds the `POST /register` handler that validates the submitted data, hashes the password, inserts the new user into the database, and redirects to the login page on success. Session management (auto-login after registration) is deferred to Step 3; this step only persists the account.

## Depends on
- Step 1 — Database Setup (`get_db()`, `init_db()`, `users` table must exist)

## Routes
- `GET /register` — render the registration form — public (already exists, no change needed)
- `POST /register` — validate form data, create user, redirect to login — public

## Database changes
No new tables or columns. The `users` table from Step 1 covers all required fields:
- `name` TEXT NOT NULL
- `email` TEXT UNIQUE NOT NULL
- `password_hash` TEXT NOT NULL

A new helper function `create_user()` must be added to `database/db.py`.

## Templates
- **Modify**: `templates/register.html`
  - Add `method="POST"` and `action="{{ url_for('register') }}"` to the `<form>` tag
  - Ensure inputs have `name` attributes: `name`, `email`, `password`, `confirm_password`
  - Display flashed error/success messages using `get_flashed_messages(with_categories=True)`
  - All links use `url_for()`

## Files to change
- `app.py` — add `POST /register` handler; import `create_user` from `database.db`; import `redirect`, `request`, `flash`, `url_for` from flask
- `database/db.py` — add `create_user(name, email, password)` function
- `templates/register.html` — wire up form attributes and flash message display

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` is already installed.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` — never stored in plain text
- Use CSS variables — never hardcode hex values in any new styles
- All templates extend `base.html`
- DB logic lives in `database/db.py` — the route function must not contain any SQL
- Use `flash()` for user-facing error and success messages; never return bare error strings
- Duplicate email must be caught and shown as a form error (catch `sqlite3.IntegrityError`)
- Password and confirm_password must match — validate in the route before calling `create_user`
- Name and email must be non-empty — validate in the route
- On success redirect to `url_for('login')` — do **not** create a session (that is Step 3)
- Use `abort()` only for HTTP-level errors, not validation failures

## Definition of done
- [ ] Visiting `/register` renders a form with fields: Name, Email, Password, Confirm Password
- [ ] Submitting the form with all valid fields creates a new row in the `users` table
- [ ] The stored `password_hash` is a werkzeug hash, not plain text
- [ ] After successful registration the user is redirected to `/login`
- [ ] Submitting with mismatched passwords shows an error message and does not insert a row
- [ ] Submitting with an already-registered email shows an error message and does not insert a duplicate row
- [ ] Submitting with any empty field shows an error message and does not insert a row
- [ ] All form action/link URLs use `url_for()` — no hardcoded paths
