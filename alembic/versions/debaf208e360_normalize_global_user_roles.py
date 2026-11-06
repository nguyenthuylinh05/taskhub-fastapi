"""normalize global user roles

Revision ID: debaf208e360
Revises: 4a5dfc1b7b75
Create Date: 2026-11-06 20:47:24.016522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'debaf208e360'
down_revision: Union[str, Sequence[str], None] = '4a5dfc1b7b75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Chuyển các tài khoản USER cũ thành MEMBER
    op.execute(
        "UPDATE users SET role = 'MEMBER' WHERE role = 'USER'"
    )

    # Cập nhật giá trị mặc định trong database
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "role",
            existing_type=sa.String(length=50),
            existing_nullable=False,
            server_default="MEMBER",
        )


def downgrade() -> None:
    # Khôi phục giá trị mặc định cũ.
    # Không chuyển MEMBER về USER vì có thể đã có tài khoản
    # MEMBER mới được đăng ký sau khi migration được áp dụng.
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "role",
            existing_type=sa.String(length=50),
            existing_nullable=False,
            server_default="USER",
        )