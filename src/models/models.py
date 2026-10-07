from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import date
from typing import List, Optional

class Base(DeclarativeBase):
    pass 

class Group(Base):
    __tablename__ = "group"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    curator_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    users: Mapped[List["User"]] = relationship(back_populates='group', foreign_keys="User.group_id")
    curator: Mapped[Optional["User"]] = relationship(foreign_keys=[curator_id])

    def __str__(self) -> str:
        return self.name

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int | None] = mapped_column(ForeignKey("group.id"), nullable=True)
    group: Mapped["Group | None"] = relationship(back_populates='users', foreign_keys=[group_id])

    def __str__(self) -> str:
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(p for p in parts if p).strip() or self.email

class Grade(Base):
    __tablename__ = "grade"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column(nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    grade_date: Mapped[date] = mapped_column(nullable=False)

    kind: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[int | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(String(100), nullable=True)

class Pair(Base):
    __tablename__ = "pairs"
    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    subject_name: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[int] = mapped_column(nullable=False)
    day: Mapped[str] = mapped_column(nullable=False)
    start: Mapped[str] = mapped_column(nullable=False)
    end: Mapped[str] = mapped_column(nullable=False)

    teacher: Mapped["User"] = relationship(foreign_keys=[teacher_id])
    group: Mapped["Group"] = relationship(foreign_keys=[group_id])