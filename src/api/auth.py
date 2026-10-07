from src.core.database import get_db
from src.models.models import User
from fastapi import APIRouter, Depends, Request, HTTPException, Response
from sqlalchemy.orm import Session
from src.schemas.schemas import UserRequest, LoginRequest
from src.core.security import security, config, verify_password

router = APIRouter(prefix="/auth")

@router.post("")
def user_login(response: Response, login: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==login.email).first()
    if user is None or not verify_password(plain=login.password, hashed=user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = security.create_access_token(uid=str(user.id))
    response.set_cookie(
    key="cookie",
    value=token,
    httponly=True,
    samesite="lax",      
    secure=False,         
    path="/",           
    )
    return {"message": token}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы вышли из системы"}