"""
Заполнение БД тестовыми данными.

Запуск (из корня проекта):
    python seed.py

⚠️ УДАЛЯЕТ все данные и создаёт заново.
⚠️ Пароли хранятся в открытом виде — только для разработки!
"""

from datetime import date, timedelta

from src.core.database import SessionLocal, engine
from src.models.models import Base, User, Group, Grade, Pair
from src.core.security import hash_password

def drop_and_create():
    """Удаляем все таблицы и создаём заново."""
    print("🗑  Удаляю старые таблицы…")
    Base.metadata.drop_all(bind=engine)
    print("✅ Создаю таблицы заново…")
    Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()

    try:
        # ============================================================
        # 1. ГРУППЫ
        # ============================================================
        print("\n👥 Создаю группы…")
        group_pk = Group(name="ПК9-26", year=2026)
        group_is = Group(name="ИС-21", year=2021)
        group_pr = Group(name="ПР-22", year=2022)
        db.add_all([group_pk, group_is, group_pr])
        db.commit()
        for g in (group_pk, group_is, group_pr):
            db.refresh(g)
        print(f"   ✅ Создано групп: 3")

        # ============================================================
        # 2. УЧИТЕЛЯ
        # ============================================================
        print("\n👨‍🏫 Создаю учителей…")
        teacher_ej = User(
            email="ejeke@lyceum.ru",
            password=hash_password("12345"),
            first_name="Елена",
            last_name="Эжеке",
            middle_name="",
            birth_date=date(1980, 5, 12),
            role="teacher",
            group_id=None,
        )
        teacher_iv = User(
            email="ivanova@lyceum.ru",
            password=hash_password("12345"),
            first_name="Ирина",
            last_name="Иванова",
            middle_name="Петровна",
            birth_date=date(1975, 3, 8),
            role="teacher",
            group_id=None,
        )
        teacher_si = User(
            email="sidorov@lyceum.ru",
            password=hash_password("12345"),
            first_name="Пётр",
            last_name="Сидоров",
            middle_name="Иванович",
            birth_date=date(1978, 11, 20),
            role="teacher",
            group_id=None,
        )
        db.add_all([teacher_ej, teacher_iv, teacher_si])
        db.commit()
        for t in (teacher_ej, teacher_iv, teacher_si):
            db.refresh(t)
        print(f"   ✅ Создано учителей: 3")

        # ============================================================
        # 3. АДМИН
        # ============================================================
        print("\n👑 Создаю админа…")
        admin = User(
            email="admin@lyceum.ru",
            password=hash_password("admin123"),
            first_name="Админ",
            last_name="Системы",
            middle_name="",
            birth_date=date(1990, 1, 1),
            role="admin",
            group_id=None,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"   ✅ Админ: {admin.email}")

        # ============================================================
        # 4. КУРАТОРЫ
        # ============================================================
        print("\n🎓 Назначаю кураторов…")
        group_pk.curator_id = teacher_ej.id
        group_is.curator_id = teacher_iv.id
        db.commit()
        print(f"   ✅ ПК9-26 → куратор {teacher_ej.last_name}")
        print(f"   ✅ ИС-21  → куратор {teacher_iv.last_name}")

        # ============================================================
        # 5. УЧЕНИКИ
        # ============================================================
        print("\n🎒 Создаю учеников…")
        students = [
            # --- ПК9-26 ---
            User(
                email="petrov@lyceum.ru",
                password=hash_password("12345"),
                first_name="Иван",
                last_name="Петров",
                middle_name="Сергеевич",
                birth_date=date(2008, 4, 15),
                role="student",
                group_id=group_pk.id,
            ),
            User(
                email="sidorova@lyceum.ru",
                password=hash_password("12345"),
                first_name="Мария",
                last_name="Сидорова",
                middle_name="Ивановна",
                birth_date=date(2008, 7, 22),
                role="student",
                group_id=group_pk.id,
            ),
            User(
                email="kuznetsov@lyceum.ru",
                password=hash_password("12345"),
                first_name="Дмитрий",
                last_name="Кузнецов",
                middle_name="Александрович",
                birth_date=date(2008, 2, 10),
                role="student",
                group_id=group_pk.id,
            ),
            # --- ИС-21 ---
            User(
                email="smirnova@lyceum.ru",
                password=hash_password("12345"),
                first_name="Анна",
                last_name="Смирнова",
                middle_name="Петровна",
                birth_date=date(2003, 9, 5),
                role="student",
                group_id=group_is.id,
            ),
            User(
                email="morozov@lyceum.ru",
                password=hash_password("12345"),
                first_name="Никита",
                last_name="Морозов",
                middle_name="Владимирович",
                birth_date=date(2003, 12, 18),
                role="student",
                group_id=group_is.id,
            ),
        ]
        db.add_all(students)
        db.commit()
        for s in students:
            db.refresh(s)
        print(f"   ✅ Создано учеников: {len(students)}")

        student_petrov = students[0]   # Иван Петров

        # ============================================================
        # 6. РАСПИСАНИЕ для ПК9-26
        # ============================================================
        print("\n📅 Заполняю расписание для ПК9-26…")
        pairs_data = [
            # Пн
            ("Пн", 1, "Программирование", teacher_ej.id, "08:00", "09:30"),
            ("Пн", 2, "Математика",       teacher_iv.id, "09:40", "11:10"),
            ("Пн", 3, "Русский язык",     teacher_si.id, "11:20", "12:50"),
            # Вт
            ("Вт", 1, "Математика",       teacher_iv.id, "08:00", "09:30"),
            ("Вт", 2, "Программирование", teacher_ej.id, "09:40", "11:10"),
            ("Вт", 3, "История",          teacher_si.id, "11:20", "12:50"),
            # Ср
            ("Ср", 1, "Русский язык",     teacher_si.id, "08:00", "09:30"),
            ("Ср", 2, "Математика",       teacher_iv.id, "09:40", "11:10"),
            ("Ср", 3, "Программирование", teacher_ej.id, "11:20", "12:50"),
            # Чт
            ("Чт", 1, "Программирование", teacher_ej.id, "08:00", "09:30"),
            ("Чт", 2, "Физика",           teacher_iv.id, "09:40", "11:10"),
            ("Чт", 3, "Математика",       teacher_iv.id, "11:20", "12:50"),
            # Пт
            ("Пт", 1, "Математика",       teacher_iv.id, "08:00", "09:30"),
            ("Пт", 2, "Английский язык",  teacher_si.id, "09:40", "11:10"),
            ("Пт", 3, "Программирование", teacher_ej.id, "11:20", "12:50"),
            # Сб
            ("Сб", 1, "История",          teacher_si.id, "08:00", "09:30"),
            ("Сб", 2, "Физическая культура", teacher_si.id, "09:40", "11:10"),
        ]

        for day, num, subj, tid, start, end in pairs_data:
            db.add(Pair(
                teacher_id=tid,
                group_id=group_pk.id,
                subject_name=subj,
                number=num,
                day=day,
                start=start,
                end=end,
            ))
        db.commit()
        print(f"   ✅ Создано пар: {len(pairs_data)}")

        # ============================================================
        # 7. ОЦЕНКИ Ивана Петрова
        # ============================================================
        print("\n📊 Выставляю оценки Ивану Петрову…")
        today = date.today()

        grades_data = [
            ("Математика",       5, 3,  "Отличная работа",  teacher_iv.id),
            ("Математика",       4, 6,  "Домашняя работа",  teacher_iv.id),
            ("Математика",       5, 10, "",                 teacher_iv.id),
            ("Программирование", 5, 2,  "Отличный проект",  teacher_ej.id),
            ("Программирование", 5, 5,  "",                 teacher_ej.id),
            ("Программирование", 4, 9,  "Минорные баги",    teacher_ej.id),
            ("Русский язык",     4, 4,  "Сочинение",        teacher_si.id),
            ("Русский язык",     5, 8,  "",                 teacher_si.id),
            ("Английский язык",  4, 5,  "",                 teacher_si.id),
            ("История",          5, 6,  "Доклад",           teacher_si.id),
            ("Физика",           4, 7,  "Лабораторная",     teacher_iv.id),
        ]

        for subj, val, days, comment, tid in grades_data:
            db.add(Grade(
                subject_name=subj,
                student_id=student_petrov.id,
                teacher_id=tid,
                grade_date=today - timedelta(days=days),
                kind="grade",
                value=val,
                status="",
                comment=comment or "",
            ))

        absences_data = [
            ("Физическая культура", "Б", 5, "Болел, справка",   teacher_si.id),
            ("История",             "Н", 8, "Прогулял",          teacher_si.id),
            ("Программирование",    "У", 12, "Уважительная",    teacher_ej.id),
        ]

        for subj, status, days, comment, tid in absences_data:
            db.add(Grade(
                subject_name=subj,
                student_id=student_petrov.id,
                teacher_id=tid,
                grade_date=today - timedelta(days=days),
                kind="absence",
                value=None,
                status=status,
                comment=comment,
            ))

        db.commit()
        print(f"   ✅ Оценок: {len(grades_data)}")
        print(f"   ✅ Пропусков: {len(absences_data)}")

        # ============================================================
        # ИТОГ
        # ============================================================
        print("\n" + "=" * 55)
        print("✅ БД успешно заполнена!")
        print("=" * 55)
        print("\n📧 ЛОГИНЫ (пароль в скобках):\n")
        print("  👑 Админ:")
        print(f"     admin@lyceum.ru           (admin123)\n")
        print("  👨‍🏫 Учителя:")
        print(f"     ejeke@lyceum.ru           (12345)   ← куратор ПК9-26")
        print(f"     ivanova@lyceum.ru         (12345)   ← куратор ИС-21")
        print(f"     sidorov@lyceum.ru         (12345)\n")
        print("  🎒 Ученики ПК9-26:")
        print(f"     petrov@lyceum.ru          (12345)   ← Иван Петров (с оценками)")
        print(f"     sidorova@lyceum.ru        (12345)   ← Мария Сидорова")
        print(f"     kuznetsov@lyceum.ru       (12345)\n")
        print("  🎒 Ученики ИС-21:")
        print(f"     smirnova@lyceum.ru        (12345)")
        print(f"     morozov@lyceum.ru         (12345)")
        print()

    except Exception as e:
        db.rollback()
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 55)
    print("🌱 SEED — заполнение БД тестовыми данными")
    print("=" * 55)
    drop_and_create()
    seed()