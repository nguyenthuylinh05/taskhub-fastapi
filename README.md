# Day 2: Database – SQLAlchemy 2.x & Alembic

## Nội dung

- **SQLAlchemy 2.x Async:** Tích hợp cơ sở dữ liệu bất đồng bộ với `AsyncEngine`, `AsyncSession` và `async_sessionmaker`.
- **Model Definition:** Xây dựng các SQLAlchemy Models gồm `User` và `Task`.
- **Relationships:** Thiết lập quan hệ One-to-Many giữa User và Task bằng `relationship()`, `back_populates` và `ForeignKey`.
- **Repository Pattern:** Xây dựng Generic `BaseRepository[T]` và `TaskRepository` để tái sử dụng các thao tác CRUD.
- **Async CRUD:** Triển khai các thao tác Create, Read, Update, Delete sử dụng SQLAlchemy Async.
- **Pagination:** Hỗ trợ phân trang danh sách Task bằng `LIMIT`, `OFFSET` và tổng số bản ghi.
- **Alembic Migration:** Khởi tạo Alembic, tự động phát hiện thay đổi Model và quản lý Database Schema.
- **FastAPI Integration:** Tích hợp Async Database Session vào FastAPI thông qua Dependency Injection.

## Database Models

- `users`: Lưu thông tin người dùng.
- `tasks`: Lưu thông tin công việc.
- Relationship: Một User có thể có nhiều Task; mỗi Task có thể thuộc về một User.

## Endpoints

**TaskHub API – Swagger UI**

Các API được tích hợp với SQLAlchemy và SQLite:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/tasks/` | List Tasks with Pagination |
| POST | `/api/v1/tasks/` | Create Task |
| GET | `/api/v1/tasks/{task_id}` | Get Task by ID |
| PATCH | `/api/v1/tasks/{task_id}` | Update Task |
| DELETE | `/api/v1/tasks/{task_id}` | Delete Task |
| GET | `/health` | Health Check |

## Database Migration

- Initialize Alembic.
- Generate migration using `--autogenerate`.
- Apply migration using `alembic upgrade head`.
- Verify migration using `alembic current` and `alembic history`.

## Testing Results

- Successfully tested Create, Read, Update and Delete operations.
- Verified HTTP `201 Created`, `200 OK` and `204 No Content`.
- Verified `404 Not Found` when requesting a deleted or non-existent Task.
- Successfully tested pagination with different `page_size` values.
- Verified database persistence after restarting the application.

---

**Result:** Completed SQLAlchemy 2.x asynchronous database integration, Model relationships, Generic Repository Pattern, CRUD operations, pagination and Alembic migrations.