from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal
import bcrypt

# ─── CONFIG ───────────────────────────────────────────────
SECRET_KEY = "tekken_secret_key_make_this_very_long_123456"
ALGORITHM  = "HS256"
TOKEN_EXPIRE_MINUTES = 60  # token expires after 60 minutes

# ─── PASSWORD HASHING ─────────────────────────────────────


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        plain.encode("utf-8"),
        hashed.encode("utf-8")
    )

# ─── TOKEN CREATE ─────────────────────────────────────────
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ─── TOKEN DECODE ─────────────────────────────────────────
def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# ─── OAUTH2 SCHEME ────────────────────────────────────────
# tells FastAPI where the token comes from
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ─── DB SESSION ───────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ─── GET CURRENT USER (THE GLOBAL DEPENDENCY) ─────────────
# import this one function in any router to protect any endpoint
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

    import model
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user