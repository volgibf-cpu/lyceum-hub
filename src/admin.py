from src.models.models import User, Group, Grade, Pair
from sqladmin import Admin, ModelView
from src.core.database import engine
from src.core.security import hash_password

# ============ User ============
class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    column_list = [
        User.id,
        User.email,
        User.first_name,
        User.last_name,
        User.middle_name,
        User.birth_date,
        User.role,
        User.group_id
    ]
        

    form_columns = [
        User.email,
        User.password,
        User.first_name,
        User.last_name,
        User.middle_name,
        User.birth_date,
        User.role,
        User.group,
    ]

    async def on_model_change(self, data, model, is_created, request):
        new_password = data.get("password")

        if new_password and not new_password.startswith("$2b$"):
            data["password"] = hash_password(new_password)


# ============ Group ============
class GroupAdmin(ModelView, model=Group):
    name = "Группа"
    name_plural = "Группы"
    icon = "fa-solid fa-users"

    column_list = [
        Group.id,
        Group.name,
        Group.year,
        Group.curator_id,
    ]

    form_columns = [
        Group.name,
        Group.year,
        Group.curator,
    ]


# ============ Grade ============
class GradeAdmin(ModelView, model=Grade):
    name = "Оценка"
    name_plural = "Оценки"
    icon = "fa-solid fa-star"

    column_list = [
        Grade.id,
        Grade.subject_name,
        Grade.student_id,
        Grade.teacher_id,
        Grade.grade_date,
        Grade.kind,
        Grade.value,
        Grade.status,
        Grade.comment,
    ]

    form_columns = [
        Grade.subject_name,
        Grade.student_id,
        Grade.teacher_id,
        Grade.grade_date,
        Grade.kind,
        Grade.value,
        Grade.status,
        Grade.comment,
    ]


# ============ Pair ============
class PairAdmin(ModelView, model=Pair):
    name = "Пара"
    name_plural = "Расписание"
    icon = "fa-solid fa-calendar"

    column_list = [
        Pair.id,
        Pair.teacher_id,
        Pair.group_id,
        Pair.subject_name,
        Pair.number,
        Pair.day,
        Pair.start,
        Pair.end,
    ]

    form_columns = [
        Pair.teacher_id,
        Pair.group_id,
        Pair.subject_name,
        Pair.number,
        Pair.day,
        Pair.start,
        Pair.end,
    ]


# ============ Setup ============
def setup_admin(app):
    admin = Admin(app=app, engine=engine, title="Проф. лицей — Админка")

    admin.add_view(UserAdmin)
    admin.add_view(GroupAdmin)
    admin.add_view(GradeAdmin)
    admin.add_view(PairAdmin)

    return admin