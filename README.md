# TaskHub - FastAPI Framework

## Giới thiệu
TaskHub là dự án thực hành xây dựng REST API
quản lý công việc bằng FastAPI.

## Day 1: Core Setup & Architecture

Nội dung:
- Layered Architecture
- FastAPI Application & APIRouter
- Lifespan Events
- Routing & Request Handling
- Dependency Injection
- Pydantic v2 Schemas
- CRUD API cho resource Task

## Công nghệ
- Python
- FastAPI
- Pydantic v2
- Uvicorn
- uv

## Hướng dẫn chạy

1. Clone repository:

   git clone https://github.com/nguyenthuylinh05/taskhub-fastapi.git

2. Vào thư mục project:

   cd taskhub-fastapi

3. Cài thư viện:

   uv sync

4. Chạy ứng dụng:

   uv run uvicorn app.main:app --reload

5. Truy cập Swagger UI:

   http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Chức năng |
|---|---|---|
| POST | /api/v1/tasks | Tạo task |
| GET | /api/v1/tasks | Lấy danh sách |
| GET | /api/v1/tasks/{task_id} | Xem chi tiết |
| PATCH | /api/v1/tasks/{task_id} | Cập nhật |
| DELETE | /api/v1/tasks/{task_id} | Xóa |

## Ghi chú
Ngày 1 dữ liệu được lưu tạm trong RAM.
Khi khởi động lại server, dữ liệu sẽ mất.

Database sẽ được tích hợp ở ngày tiếp theo.
