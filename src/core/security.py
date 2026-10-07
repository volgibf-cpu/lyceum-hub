from authx import AuthX, AuthXConfig
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

config = AuthXConfig()
config.JWT_ACCESS_COOKIE_NAME = "cookie"
config.JWT_SECRET_KEY = SECRET_KEY
config.JWT_TOKEN_LOCATION = ["cookies", "headers"]
config.JWT_COOKIE_CSRF_PROTECT = False

security = AuthX(config=config)

def get_token_from_cookies(request) -> int:
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    payload = security._decode_token(token)
    uid = int(payload.sub)
    return uid

def get_token_from_headers(request) -> int:
    headers = request.heders.get("Authorization")
    token = headers.split(" ")[1]
    payload = security._decode_token(token)
    uid = int(payload.sub)
    return uid

def hash_password(password: str) -> str: 
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))