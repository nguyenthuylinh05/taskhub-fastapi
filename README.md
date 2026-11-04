# TaskHub - FastAPI Framework Practical Project

## Day 4: Authorization & RBAC

### Nội dung

- **Role-Based Access Control (RBAC):** Xây dựng cơ chế phân quyền dựa trên vai trò người dùng (`ADMIN`, `USER`).
- **Role Authorization Dependency:** Xây dựng `require_roles()` để kiểm tra quyền truy cập dựa trên vai trò được cho phép.
- **Admin-Only Endpoint:** Bảo vệ endpoint `/api/v1/users/admin`, chỉ cho phép người dùng có vai trò `ADMIN` truy cập.
- **Resource Ownership:** Đảm bảo mỗi người dùng chỉ có thể truy cập và thao tác trên các Task thuộc quyền sở hữu của mình.
- **Automatic Task Ownership:** Tự động gán `user_id` của người đang đăng nhập khi tạo Task.
- **Owner-Based Query:** Lọc danh sách và đếm số lượng Task theo `user_id`.
- **Protected CRUD Operations:** Kiểm tra quyền sở hữu trước khi xem chi tiết, cập nhật hoặc xóa Task.

### Authorization Components

| Component | Description |
|---|---|
| `require_roles()` | Kiểm tra vai trò người dùng |
| `CurrentUser` | Lấy người dùng hiện tại đã xác thực |
| `get_by_id_for_user()` | Truy vấn Task theo ID và chủ sở hữu |
| `get_all_for_user()` | Lấy danh sách Task của một người dùng |
| `count_for_user()` | Đếm số Task thuộc về một người dùng |

### Resource Ownership Flow

1. Client gửi request kèm JWT Access Token.
2. `get_current_user` xác thực token và lấy thông tin người dùng.
3. Khi tạo Task, hệ thống tự động gán `user_id` từ người dùng hiện tại.
4. Khi truy vấn danh sách Task, hệ thống chỉ lấy dữ liệu có `user_id` tương ứng.
5. Khi xem, cập nhật hoặc xóa Task, hệ thống kiểm tra đồng thời `task_id` và `user_id`.
6. Nếu Task không tồn tại hoặc không thuộc quyền sở hữu của người dùng, API trả về `404 Not Found`.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/users/admin` | Admin-only endpoint |
| POST | `/api/v1/tasks` | Create Task with automatic ownership |
| GET | `/api/v1/tasks` | Get current user's Tasks |
| GET | `/api/v1/tasks/{task_id}` | Get an owned Task |
| PATCH | `/api/v1/tasks/{task_id}` | Update an owned Task |
| DELETE | `/api/v1/tasks/{task_id}` | Delete an owned Task |

### Testing Results

- Successfully tested `ADMIN` access to `/api/v1/users/admin` with `200 OK`.
- Verified `403 Forbidden` when a `USER` accesses the admin-only endpoint.
- Successfully tested automatic assignment of `user_id` when creating a Task.
- Verified that users can only retrieve their own Tasks.
- Successfully tested pagination with user-specific filtering and counting.
- Verified `404 Not Found` when accessing another user's Task.
- Verified `404 Not Found` when attempting to update or delete another user's Task.
- Successfully tested Task ownership isolation using two different user accounts.

**Result:** Completed role-based access control (RBAC), authorization dependencies, admin-only endpoint protection and resource ownership enforcement for Task CRUD operations.

---

## Công nghệ

- Python
- FastAPI
- Pydantic v2
- Pydantic Settings
- SQLAlchemy 2.x Async
- Alembic
- SQLite
- Passlib
- Bcrypt
- PyJWT
- Uvicorn
- uv

## Hướng dẫn chạy

1. Clone repository:

```bash
git clone https://github.com/nguyenthuylinh05/taskhub-fastapi.git
```

2. Vào thư mục project:

```bash
cd taskhub-fastapi
```

3. Cài đặt dependencies:

```bash
uv sync
```

4. Tạo file `.env` từ cấu hình mẫu và thiết lập `JWT_SECRET_KEY` riêng.

5. Chạy database migration:

```bash
uv run alembic upgrade head
```

6. Khởi động ứng dụng:

```bash
uv run uvicorn app.main:app --reload
```

7. Truy cập Swagger UI:

http://127.0.0.1:8000/docs

---

**Result:** Completed asynchronous database integration, SQLAlchemy ORM, Alembic migrations, user registration, password hashing, JWT authentication and protected API endpoints.
