# TaskHub - FastAPI Framework Practical Project

## Day 3: Authentication & Security

### Nội dung

- **Environment Configuration:** Sử dụng `Pydantic Settings` để quản lý cấu hình ứng dụng và tải biến môi trường từ file `.env`.
- **User Model Enhancement:** Bổ sung các trường `hashed_password`, `role`, `is_active` và `created_at` vào User Model.
- **Alembic Migration:** Tạo và thực thi migration để cập nhật cấu trúc bảng `users`.
- **Password Hashing:** Sử dụng `Passlib` và `Bcrypt` để mã hóa mật khẩu trước khi lưu vào database.
- **Password Verification:** Kiểm tra mật khẩu người dùng bằng hàm `verify_password()`.
- **User Registration:** Xây dựng API đăng ký tài khoản, kiểm tra email trùng lặp và lưu mật khẩu dưới dạng hash.
- **User Login:** Xây dựng API đăng nhập và xác thực thông tin tài khoản.
- **JWT Authentication:** Sử dụng `PyJWT` để tạo, giải mã và xác thực JSON Web Token (JWT) Access Token.
- **Authentication Dependency:** Xây dựng `get_current_user` để xác thực Bearer Token và truy xuất người dùng từ database.
- **Protected Endpoint:** Bảo vệ API bằng cơ chế JWT Authentication.
- **Swagger Integration:** Tích hợp HTTP Bearer Authentication để kiểm thử các API yêu cầu đăng nhập.

### User Model

Bổ sung các trường phục vụ xác thực và quản lý tài khoản:

| Field | Type | Description |
|---|---|---|
| `hashed_password` | String(255) | Mật khẩu đã được mã hóa |
| `role` | String(50) | Vai trò người dùng, mặc định là `USER` |
| `is_active` | Boolean | Trạng thái hoạt động của tài khoản |
| `created_at` | DateTime | Thời điểm tạo tài khoản |

### Authentication Flow

1. Người dùng gửi thông tin đăng ký thông qua Register API.
2. Hệ thống kiểm tra email và mã hóa mật khẩu bằng Bcrypt.
3. Thông tin tài khoản được lưu vào database.
4. Người dùng gửi email và mật khẩu thông qua Login API.
5. Hệ thống xác thực thông tin đăng nhập và tạo JWT Access Token.
6. Client gửi JWT trong HTTP Header theo định dạng `Authorization: Bearer <token>`.
7. `get_current_user` xác thực token, lấy User ID và truy xuất người dùng từ database.
8. Nếu hợp lệ, người dùng được phép truy cập các API được bảo vệ.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Authenticate user and generate JWT |
| GET | `/api/v1/users/me` | Get current authenticated user |

### Security Components

- **Pydantic Settings:** Quản lý `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM` và `ACCESS_TOKEN_EXPIRE_MINUTES`.
- **Passlib / Bcrypt:** Hash và verify mật khẩu.
- **PyJWT:** Encode và decode JWT Access Token.
- **HTTPBearer:** Nhận Bearer Token từ HTTP Authorization Header.
- **get_current_user:** Kiểm tra JWT, xác định người dùng và trạng thái tài khoản.
- **UserResponse:** Chỉ trả về thông tin công khai của User, không tiết lộ `hashed_password`.

### Testing Results

- Successfully tested user registration with valid information.
- Verified `409 Conflict` when registering with an existing email.
- Verified `422 Unprocessable Entity` when input data violates schema validation.
- Successfully tested login with valid credentials and JWT generation.
- Verified `401 Unauthorized` when login credentials are incorrect.
- Successfully tested JWT decoding and signature validation.
- Successfully tested protected endpoint `/api/v1/users/me` with a valid Bearer Token.
- Verified `401 Unauthorized` when no token is provided.
- Verified `401 Unauthorized` when using an invalid or expired token.
- Verified JWT-based authentication through Swagger UI.

### Configuration

Các biến môi trường được quản lý trong file `.env`:

```env
DATABASE_URL=sqlite+aiosqlite:///./taskhub.db
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Security Note:** File `.env` chứa thông tin cấu hình nhạy cảm và không được đưa lên Git repository. Sử dụng `.env.example` để cung cấp cấu hình mẫu.

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
