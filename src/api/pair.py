from src.core.database import get_db
from src.models.models import User, Pair
from fastapi import APIRouter, Depends, Request, HTTPException, Response
from sqlalchemy.orm import Session
from src.schemas.schemas import PairResponse
from src.core.security import security, config, get_token_from_cookies

router = APIRouter(prefix="/pair")

@router.get("/", dependencies=[Depends(security.access_token_required)])
def get_schedule(request: Request, db: Session = Depends(get_db)):
    
    uid = get_token_from_cookies(request=request)
    user = db.query(User).filter(User.id==uid).first()

    query = db.query(Pair, User).join(User, Pair.teacher_id == User.id)

    if user.role == "student":
        if user.group_id is None:
            raise HTTPException(status_code=404, detail="Ученик не привязан к группе")
        query = query.filter(Pair.group_id == user.group_id)
    elif user.role == "teacher":
        query = query.filter(Pair.teacher_id == user.id)

    rows = query.all()

    result = []
    for pair, teacher in rows:
        result.append({
            "teacher_id": pair.teacher_id,
            "teacher": f"{teacher.last_name} {teacher.first_name}.{teacher.middle_name}.",
            "subject_name": pair.subject_name,
            "number": pair.number,
            "day": pair.day,
            "start": pair.start,
            "end": pair.end,
        })
    return result

