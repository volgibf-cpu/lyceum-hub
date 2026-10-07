from src.core.database import get_db
from src.models.models import User, Group
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from src.schemas.schemas import UserResponse
from src.core.security import security, get_token_from_cookies

router = APIRouter(prefix="/users")

@router.get("/me", dependencies=[Depends(security.access_token_required)])
def get_data(request: Request, db: Session = Depends(get_db)):
    uid = get_token_from_cookies(request=request)
    
    user = db.query(User).filter(User.id==uid).first()

    group_name = None
    if user.role == "student":
        if user.group_id is None:
            group_name = {"message": "Ученик не привязан к группе"}
        else:
            group = db.query(Group).filter(Group.id==user.group_id).first()
            group_name = group.name 

    elif user.role == "teacher":
            group = db.query(Group).filter(Group.curator_id==user.id).first()
            group_name = group.name if group else None

    user_data = {"id": user.id,
                "email": user.email,
                "name": user.first_name,
                "second_name": user.last_name,
                "patronymic": user.middle_name,
                "group": group_name,
                "role": user.role}

    return user_data

@router.get("/student", dependencies=[Depends(security.access_token_required)])
def get_students(group_name: str, request: Request, db: Session = Depends(get_db)):
    uid = get_token_from_cookies(request=request)

    user_check = db.query(User).filter(User.id==uid).first()

    if user_check.role == "student":
        raise HTTPException(status_code=403, detail="Forbidden")

    group_list = db.query(Group).filter(Group.name==group_name).first()
    
    if group_list is None:
        raise HTTPException(status_code=404, detail="Not found")

    return [UserResponse.model_validate(user) for user in group_list.users]




          

    
