# Issue Tracker API

Build a working FastAPI service that lets a team create projects, file issues, assign work, comment, and move issues through a status workflow.

This repo starts empty. You implement everything listed below.

## Tech stack

Use what you learned in the course:

- Python 3.11+
- FastAPI
- Pydantic for request/response schemas
- SQLAlchemy or SQLModel
- SQLite for local development
- JWT authentication (OAuth2 password flow)
- Passlib / bcrypt for password hashing

A frontend is **not** required. Swagger UI (`/docs`) is enough to demo the APIs.

---

## What you have to complete

Work through these five items in order. Each one is a required deliverable.

### 1. Features of the application

Implement all of the following. Mark each as done in your own notes when it works end to end.

**Users and roles**

- [ ] Register and login
- [ ] Roles: `admin` and `member`
- [ ] Logged-in user can view `/users/me`
- [ ] Admin can list users

**Projects**

- [ ] Admin can create a project (name, description)
- [ ] Admin can add or remove project members
- [ ] Members can list projects they belong to
- [ ] Get one project with its members

**Issues**

- [ ] Project member can create an issue (title, description, priority, labels)
- [ ] Priority: `low`, `medium`, `high`
- [ ] Status: `open` → `in_progress` → `in_review` → `done` (and `closed`)
- [ ] Assign / unassign an issue to a **project member**
- [ ] Update title, description, priority, labels
- [ ] List issues for a project with filters: status, assignee, priority
- [ ] Get one issue with comments
- [ ] Soft-close an issue (`closed`); allow reopen to `open`

**Comments**

- [ ] Project member can add a comment on an issue
- [ ] List comments on an issue (newest last)
- [ ] Author can edit or delete their own comment

Do **not** build boards, file attachments, or email notifications.

### 2. Business logic

Put rules in a service layer (not only inside route functions). The API must reject invalid actions with a clear error.

- [ ] Only **project members** (or admin) can create issues, comment, or change issues in that project
- [ ] Assignee must be a member of the same project
- [ ] Issue numbers are unique **per project** (`PROJ-1`, `PROJ-2` or integer `1`, `2` scoped to the project)
- [ ] Status changes must follow the allowed flow (no skipping, e.g. `open` → `done` is invalid)
- [ ] `closed` issues cannot be edited or reassigned until reopened
- [ ] Reopen is only allowed from `closed` → `open`
- [ ] Only the **assignee**, a project admin, or global `admin` can change status
- [ ] Title is required and cannot be blank
- [ ] Deleting a project is not allowed if it still has issues (or you implement a clear cascade and document it)
- [ ] Users cannot see projects they are not members of (except global `admin`)

Write a short `BUSINESS_RULES.md` (or a section in your PR) listing these rules and which function enforces each one.

### 3. API design

Design REST APIs before you code. Keep resource names plural, use proper HTTP methods, and return consistent JSON.

Suggested shape (you may refine names, but keep this coverage):

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `POST` | `/auth/register` | public | Create user |
| `POST` | `/auth/login` | public | Get access token |
| `GET` | `/users/me` | logged in | Current user |
| `GET` | `/users` | admin | List users |
| `POST` | `/projects` | admin | Create project |
| `GET` | `/projects` | logged in | Projects the user can access |
| `GET` | `/projects/{id}` | member / admin | Project detail |
| `POST` | `/projects/{id}/members` | admin | Add member |
| `DELETE` | `/projects/{id}/members/{user_id}` | admin | Remove member |
| `POST` | `/projects/{id}/issues` | member | Create issue |
| `GET` | `/projects/{id}/issues` | member | List / filter issues |
| `GET` | `/issues/{id}` | member | Issue + comments |
| `PATCH` | `/issues/{id}` | member | Update fields |
| `POST` | `/issues/{id}/assign` | member | Assign / unassign |
| `POST` | `/issues/{id}/status` | assignee / admin | Change status |
| `POST` | `/issues/{id}/comments` | member | Add comment |
| `PATCH` | `/comments/{id}` | author | Edit comment |
| `DELETE` | `/comments/{id}` | author | Delete comment |

Requirements:

- [ ] Request and response models with Pydantic (no raw dicts as API contract)
- [ ] Nested resources where it helps (`/projects/{id}/issues`), not query-only for parent id
- [ ] Filters as query params (`?status=open&assignee_id=3`)
- [ ] Pagination on list endpoints (`skip` / `limit` or `page` / `size`)
- [ ] OpenAPI tags so `/docs` is readable
- [ ] Status codes: `201` on create, `200` on read/update, `204` on delete with no body
- [ ] Include a sample request/response for each endpoint in `/docs` (Pydantic examples or a `requests.http` file)

### 4. Error handling

Do not leak stack traces. Every failure should be a JSON body the client can display.

- [ ] One error response shape, for example: `{ "detail": "...", "code": "INVALID_STATUS_TRANSITION" }`
- [ ] Custom exceptions for business rules (not generic `Exception`)
- [ ] FastAPI exception handlers for those exceptions
- [ ] `401` when token is missing or invalid
- [ ] `403` when the user is logged in but not a member / not allowed to change status
- [ ] `404` when project, issue, or comment does not exist (do not leak that a private project exists if you can avoid it)
- [ ] `400` or `409` for rule violations (invalid status jump, assignee not in project, edit on closed issue)
- [ ] `422` for Pydantic validation (missing title, invalid enum)
- [ ] Do not return SQL errors or internal paths to the client

Add a few failing examples in `/docs` or a short `ERROR_CASES.md`.

### 5. Authentication

- [ ] `POST /auth/register` stores a **hashed** password (never plain text)
- [ ] `POST /auth/login` returns a JWT access token
- [ ] Protected routes use `Authorization: Bearer <token>`
- [ ] Dependency for `get_current_user`
- [ ] Role checks: `admin` vs `member`, plus **project membership** checks
- [ ] Only `register` and `login` are public
- [ ] Token expiry (e.g. 30–60 minutes)
- [ ] First registered user may be promoted to `admin` (document how an admin is created)
- [ ] Secrets in `.env`, not in source (keep `.env.example` with dummy values)
