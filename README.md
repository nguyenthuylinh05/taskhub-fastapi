# TaskHub - FastAPI Framework Practical Project

**TaskHub** is a task management REST API built with FastAPI, SQLAlchemy 2.x Async, Pydantic v2, and Alembic. The project focuses on clean architecture, asynchronous database operations, authentication, authorization, and Role-Based Access Control (RBAC).

## Project Overview

TaskHub is developed as a practical project to learn and implement backend development with FastAPI through a structured multi-day roadmap.

### Development Progress

| Day | Topic | Main Implementation | Status |
|---|---|---|---|
| Day 1 | Core Setup & Architecture | FastAPI application, APIRouter, dependency injection, Pydantic schemas, layered architecture, basic CRUD | Completed |
| Day 2 | Database & ORM | SQLAlchemy 2.x Async, database models, repositories, pagination, Alembic migrations | Completed |
| Day 3 | Authentication & Security | Password hashing, JWT access and refresh tokens, registration, login, logout, profile and password management | Completed |
| Day 4 | Authorization & RBAC | Global roles, Workspace roles, authorization dependencies, resource ownership, Workspace membership management | Implemented and tested |

---

## Day 1: Core Setup & Architecture

Implemented the initial FastAPI application structure and backend architecture.

### Main Features

- Created the FastAPI application instance.
- Configured application lifespan.
- Organized API routes using `APIRouter`.
- Implemented dependency injection using FastAPI `Depends`.
- Defined request and response schemas using Pydantic v2.
- Separated application components into API, core, models, repositories, schemas, and services.
- Implemented basic CRUD operations for Tasks.

### Architecture

The project follows a layered architecture:

| Layer | Responsibility |
|---|---|
| API | Handles HTTP requests and responses |
| Dependencies | Provides reusable dependencies and services |
| Services | Contains business logic |
| Repositories | Handles database queries and persistence |
| Models | Defines SQLAlchemy database models |
| Schemas | Validates request data and serializes responses |
| Core | Contains configuration, database setup, and security utilities |

---

## Day 2: Database & ORM

Implemented asynchronous database integration using SQLAlchemy 2.x and Alembic.

### Main Features

- Configured SQLAlchemy asynchronous engine and session management.
- Created declarative base models.
- Implemented database models for Users and Tasks.
- Implemented asynchronous repository operations.
- Created reusable repository functionality.
- Implemented pagination.
- Configured Alembic for database schema versioning.
- Created and applied database migrations.
- Verified database CRUD operations.

### Database Components

| Component | Description |
|---|---|
| `Base` | Declarative base for SQLAlchemy models |
| `AsyncSessionLocal` | Creates asynchronous database sessions |
| `get_db()` | Provides database sessions through dependency injection |
| `BaseRepository` | Reusable database operations |
| `TaskRepository` | Handles Task database queries |
| `UserRepository` | Handles User database queries |
| Alembic | Manages database schema migrations |

---

## Day 3: Authentication & Security

Implemented authentication and account security using password hashing and JWT.

### Main Features

- User registration.
- Password hashing using Passlib and Bcrypt.
- User login and credential verification.
- JWT access token generation.
- JWT refresh token generation.
- Refresh token storage in the database.
- Refresh token rotation.
- Logout and refresh token revocation.
- Current user authentication using HTTP Bearer tokens.
- Retrieve user profile.
- Update user profile.
- Change password.
- Revoke existing refresh tokens after password changes.
- Prevent inactive users from accessing protected endpoints.

### Authentication Components

| Component | Description |
|---|---|
| `security.py` | Password hashing and JWT utilities |
| `AuthService` | Handles registration, login, refresh, and logout |
| `UserService` | Handles profile and password operations |
| `RefreshTokenRepository` | Manages refresh token persistence and revocation |
| `get_current_user()` | Validates access tokens and retrieves the authenticated user |
| `CurrentUser` | Dependency for accessing the authenticated user |

### Authentication API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Authenticate user and issue tokens |
| POST | `/api/v1/auth/refresh` | Refresh access token and rotate refresh token |
| POST | `/api/v1/auth/logout` | Revoke refresh token |
| GET | `/api/v1/users/me` | Retrieve current user profile |
| PATCH | `/api/v1/users/me` | Update current user profile |
| POST | `/api/v1/users/me/change-password` | Change current user password |

*Note: The exact HTTP method and path for profile and password endpoints should match the current API router implementation.*

### Security Implementation

- Passwords are stored as hashes instead of plaintext.
- Access tokens are validated using JWT.
- Refresh tokens are stored securely as hashes.
- Refresh token rotation prevents reuse of consumed refresh tokens.
- Password changes revoke the user's existing refresh tokens.
- User registration assigns the default global role `MEMBER`; clients cannot assign themselves the `ADMIN` role.

---

## Day 4: Authorization & Role-Based Access Control (RBAC)

Implemented authorization mechanisms at both the system level and Workspace level.

### 1. Global Role-Based Access Control

Defined global roles using `app/core/roles.py`.

| Global Role | Description |
|---|---|
| `ADMIN` | System administrator with administrative access |
| `MEMBER` | Standard registered user |

Implemented `require_roles()` to restrict access to endpoints based on allowed global roles.

### 2. Workspace Role-Based Access Control

Introduced Workspace and Workspace Member entities to support resource-level permissions.

| Workspace Role | Description |
|---|---|
| `OWNER` | Owns the Workspace and manages its members |
| `EDITOR` | Can access the Workspace and view its members |
| `VIEWER` | Can access the Workspace and view its members |

Global roles and Workspace roles are independent. A user can have the global role `MEMBER` and a Workspace role such as `OWNER`, `EDITOR`, or `VIEWER`.

A global `ADMIN` has administrative access that bypasses normal Workspace membership restrictions.

### 3. Workspace Management

Implemented Workspace operations:

- Create a Workspace.
- Retrieve the current user's Workspaces.
- Retrieve Workspace details.
- Delete a Workspace.
- Automatically assign the creator as the primary Workspace owner.
- Automatically create an `OWNER` membership when a Workspace is created.

### 4. Workspace Member Management

Implemented member management with role-based authorization:

- List Workspace members.
- Add an existing registered user to a Workspace.
- Assign `EDITOR` or `VIEWER` when adding a member.
- Update an existing member's Workspace role.
- Remove a member from a Workspace.
- Prevent duplicate memberships.
- Prevent removal or demotion of the primary Workspace owner.
- Prevent removal of the last remaining `OWNER`.

### 5. Resource Ownership

Implemented Task ownership isolation.

- Automatically associate a Task with its owner.
- Retrieve Tasks belonging to the authenticated user.
- Filter Task queries by `user_id`.
- Count Tasks belonging to the authenticated user.
- Check Task ownership before retrieving, updating, or deleting a Task.
- Return `404 Not Found` when a Task does not exist or does not belong to the current user.

### Authorization Components

| Component | Description |
|---|---|
| `GlobalRole` | Defines system-level roles |
| `WorkspaceRole` | Defines Workspace-level roles |
| `require_roles()` | Checks allowed global roles |
| `get_current_user()` | Authenticates the current user |
| `CurrentUser` | Provides the authenticated user |
| `WorkspaceService` | Implements Workspace business logic and authorization |
| `WorkspaceRepository` | Handles Workspace database queries |
| `WorkspaceMemberRepository` | Handles Workspace membership queries |
| `get_by_id_for_user()` | Retrieves a Workspace accessible to a user |
| `get_all_for_user()` | Retrieves Workspaces associated with a user |
| `get_by_workspace_and_user()` | Retrieves a user's membership in a Workspace |
| `count_owners()` | Counts Workspace owners |

### Workspace API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/workspaces` | Create a Workspace |
| GET | `/api/v1/workspaces` | List current user's Workspaces |
| GET | `/api/v1/workspaces/{workspace_id}` | Retrieve Workspace details |
| DELETE | `/api/v1/workspaces/{workspace_id}` | Delete a Workspace |
| GET | `/api/v1/workspaces/{workspace_id}/members` | List Workspace members |
| POST | `/api/v1/workspaces/{workspace_id}/members` | Add a Workspace member |
| PATCH | `/api/v1/workspaces/{workspace_id}/members/{user_id}` | Update a member's role |
| DELETE | `/api/v1/workspaces/{workspace_id}/members/{user_id}` | Remove a Workspace member |

### Authorization Testing Results

The following tests were performed using Swagger UI with different user accounts and access tokens.

#### Global and Workspace Roles

- Verified that a newly registered user receives the default global role `MEMBER`.
- Verified that the global role `ADMIN` is independent of Workspace roles.
- Verified that a Workspace creator automatically receives the `OWNER` role.
- Successfully added members with `EDITOR` and `VIEWER` roles.

#### EDITOR Permission Tests

- Successfully retrieved Workspace details.
- Successfully retrieved Workspace member lists.
- Verified `403 Forbidden` when attempting to add members.
- Verified `403 Forbidden` when attempting to update member roles.
- Verified `403 Forbidden` when attempting to remove members.

#### VIEWER Permission Tests

- Successfully retrieved Workspace details.
- Successfully retrieved Workspace member lists.
- Verified `403 Forbidden` when attempting to add members.
- Verified `403 Forbidden` when attempting to update member roles.
- Verified `403 Forbidden` when attempting to remove members.

#### OWNER Permission Tests

- Successfully added Workspace members.
- Successfully updated member roles.
- Successfully removed Workspace members.
- Verified that the primary Workspace owner cannot be demoted.
- Verified that the primary Workspace owner cannot be removed.

#### Expected HTTP Responses

| HTTP Status | Description | Test Scenario |
|---|---|---|
| `200 OK` | Successful request | Retrieve Workspace, list members, update member role |
| `201 Created` | Resource created | Create Workspace or add member |
| `204 No Content` | Successful deletion | Delete Workspace member |
| `403 Forbidden` | Permission denied | EDITOR or VIEWER attempts member management |
| `404 Not Found` | Resource unavailable | Workspace or Task not found or inaccessible |
| `409 Conflict` | Operation conflicts with business rules | Duplicate membership or attempt to remove/demote primary owner |
| `422 Unprocessable Content` | Request validation failed | Missing or invalid request fields |

**Day 4 Result:** Successfully implemented and tested global authorization, Workspace-level RBAC, Task ownership isolation, and Workspace member management.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Backend REST API framework |
| Pydantic v2 | Request validation and response serialization |
| Pydantic Settings | Application configuration |
| SQLAlchemy 2.x Async | Asynchronous ORM |
| Alembic | Database migrations |
| SQLite | Development database |
| Passlib | Password hashing utilities |
| Bcrypt | Password hashing algorithm |
| PyJWT | JWT token generation and validation |
| Uvicorn | ASGI server |
| uv | Python dependency and project management |
| HTTP Bearer | API authentication scheme |

---

## Project Structure

```text
taskhub/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── tasks.py
│   │   │   ├── users.py
│   │   │   └── workspaces.py
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── roles.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── refresh_token.py
│   │   ├── workspace.py
│   │   ├── workspace_member.py
│   │   └── __init__.py
│   │
│   ├── repositories/
│   │   ├── base.py
│   │   ├── task_repository.py
│   │   ├── user_repository.py
│   │   ├── refresh_token_repository.py
│   │   ├── workspace_repository.py
│   │   └── workspace_member_repository.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── pagination.py
│   │   ├── task.py
│   │   ├── user.py
│   │   └── workspace.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   ├── user_service.py
│   │   └── workspace_service.py
│   │
│   └── main.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/nguyenthuylinh05/taskhub-fastapi.git
```

### 2. Navigate to the project directory

```bash
cd taskhub-fastapi
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Configure the required environment variables:

```env
DATABASE_URL=sqlite+aiosqlite:///./taskhub.db

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Use a unique and secure JWT secret key in your local environment. Do not commit the actual `.env` file to Git.

### 5. Apply database migrations

```bash
uv run alembic upgrade head
```

### 6. Start the development server

```bash
uv run uvicorn app.main:app --reload
```

### 7. Access API documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Database Migrations

Alembic is used to manage database schema changes.

Useful commands:

```bash
# Generate a migration
uv run alembic revision --autogenerate -m "migration_description"

# Apply all migrations
uv run alembic upgrade head

# Check current migration
uv run alembic current

# View migration history
uv run alembic history

# Roll back one migration
uv run alembic downgrade -1
```

---

## Development & Testing

Compile the application:

```bash
uv run python -m compileall app
```

Check Git working tree:

```bash
git status
```

Run the application:

```bash
uv run uvicorn app.main:app --reload
```

Use Swagger UI to test API endpoints, authentication, authorization, request validation, and response status codes.

---

## Git Branches

The project uses separate branches to organize development by day.

| Branch | Description |
|---|---|
| `main` | Main project branch |
| `day-1-core-setup` | Core setup and architecture |
| `day-2-database` | SQLAlchemy and database integration |
| `day-3-auth` | Authentication and security |
| `day-4-authorization` | Authorization and RBAC |

### Day 4 Commits

```text
231f9a6 Day 4: Add RBAC migrations and configuration updates
e969971 Day 4: Implement workspace authorization and RBAC
```

---

## Current Project Status

**Completed:**
- Core FastAPI application architecture.
- Asynchronous database integration.
- SQLAlchemy models and Alembic migrations.
- User registration and authentication.
- JWT access and refresh token management.
- Password hashing and password management.
- Task ownership enforcement.
- Global role authorization.
- Workspace creation and management.
- Workspace membership management.
- Workspace-level RBAC for OWNER, EDITOR, and VIEWER.
- Authorization testing using Swagger UI.

**Further Development:**
- Project management and Project-level permissions.
- Full TaskHub domain relationships between Workspaces, Projects, and Tasks.
- Redis caching and cache invalidation.
- Middleware and centralized exception handling improvements.
- Background task notifications.
- Docker Compose deployment.
- Logging and additional automated tests.
- Ruff and mypy quality checks.

