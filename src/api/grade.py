from src.core.database import get_db
from src.models.models import User, Grade, Group
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.schemas.schemas import GradeRequest
from src.core.security import security, get_token_from_cookies

router = APIRouter(prefix="/grade")

@router.post("/set", dependencies=[Depends(security.access_token_required)])
def set_grade(request: Request, grade: GradeRequest, db: Session = Depends(get_db)):
    uid = get_token_from_cookies(request=request)
    
    user = db.query(User).filter(User.id==uid).first()

    if user.role == "student":
        raise HTTPException(status_code=403, detail="Forbidden")

    db.add(Grade(subject_name=grade.subject_name,
                 student_id=grade.student_id,
                 teacher_id=user.id,
                 grade_date=grade.date,
                 kind=grade.kind,
                 value=grade.value,
                 status=grade.status,
                 comment=grade.comment))
    db.commit()
    return {"message": "Оценка успешно выставлена!"}

@router.get("/group", dependencies=[Depends(security.access_token_required)])
def get_students_grades(request: Request, group_name: str = None, db: Session = Depends(get_db)):

    uid = get_token_from_cookies(request=request)

    check_user = db.query(User).filter(User.id==uid).first()

    if check_user.role == "student":
        raise HTTPException(status_code=403, detail="Forbbiden")

    grades = db.query(User, Grade, Group).join(User, Grade.student_id==User.id).join(Group, User.group_id==Group.id).all() 

    result = [
        {
            "id": grade.id,
            "student_id": user.id,
            "student": f"{user.last_name} {user.first_name[0]}.",
            "subject_name": grade.subject_name,
            "value": grade.value,
            "kind": grade.kind,
            "status": grade.status,
            "date": str(grade.grade_date),
            "comment": grade.comment or "",
            "group": group.name,
        }
        for user, grade, group in grades
    ]

    return result

@router.get("/student", dependencies=[Depends(security.access_token_required)])
def get_student_grade(request: Request, user_id: int, db: Session = Depends(get_db)):

    uid = get_token_from_cookies(request=request)
    
    check_user = db.query(User).filter(User.id==uid).first()
    
    if check_user.role == "student":
        raise HTTPException(status_code=403, detail="Forbbiden") 

    grades = db.query(Grade).filter(Grade.student_id == user_id).all()

    student = db.query(User).filter(User.id == user_id).first()

    teacher_ids = {g.teacher_id for g in grades}

    teachers = (
        db.query(User).filter(User.id.in_(teacher_ids)).all()
        if teacher_ids else []
    )
    teachers_map = {t.id: t for t in teachers}

    results = [
        {
            "id": g.id,
            "student_id": g.student_id,
            "student": (
                f"{student.last_name} {student.first_name[0]}."
                if student else "—"
            ),
            "subject_name": g.subject_name,
            "kind": g.kind,
            "value": g.value,
            "status": g.status,
            "date": str(g.grade_date),
            "comment": g.comment or "",
            "teacher": (
                f"{teachers_map[g.teacher_id].last_name} "
                f"{teachers_map[g.teacher_id].first_name[0]}."
                if g.teacher_id in teachers_map
                else "—"
            ),
        }
        for g in grades
    ]

    return results


@router.get("/me")
def get_my_grades(request: Request, db: Session = Depends(get_db)):
    uid = get_token_from_cookies(request=request)

    check_user = db.query(User).filter(User.id==uid).first()

    if check_user is None:
        raise HTTPException(status_code=401, detail="User not found")

    grades = db.query(User, Grade).join(User, Grade.teacher_id==User.id).filter(Grade.student_id==uid).all()

    results = [
        {
            "id": grade.id,
            "subject_name": grade.subject_name,
            "kind": grade.kind,
            "value": grade.value,
            "status": grade.status,
            "date": str(grade.grade_date),
            "comment": grade.comment or "",
            "teacher": f"{user.last_name} {user.first_name[0]}"
        } for user, grade in grades
        ]

    return results


    

    


