"""initial migration

Revision ID: b56b8797c482
Revises: 
Create Date: 2023-12-01 07:44:52.200407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b56b8797c482"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "DEPARTMENT",
        sa.Column("code", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("code"),
    )
    op.create_table(
        "USER",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("real_name", sa.String(length=255), nullable=False),
        sa.Column(
            "user_type",
            sa.Enum("student", "instructor", name="user_type"),
            nullable=False,
        ),
        sa.Column("department_code", sa.Integer(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["department_code"],
            ["DEPARTMENT.code"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "COURSE",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_name", sa.String(length=255), nullable=False),
        sa.Column("course_description", sa.String(length=1024), nullable=False),
        sa.Column("course_capacity", sa.Integer(), nullable=False),
        sa.Column("department_code", sa.Integer(), nullable=False),
        sa.Column("professor_id", sa.Integer(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["department_code"],
            ["DEPARTMENT.code"],
        ),
        sa.ForeignKeyConstraint(
            ["professor_id"],
            ["USER.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ENROLLMENT",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("enrollment_time", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column(
            "created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["COURSE.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["USER.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ENROLLMENT")
    op.drop_table("COURSE")
    op.drop_table("USER")
    op.drop_table("DEPARTMENT")
    # ### end Alembic commands ###
