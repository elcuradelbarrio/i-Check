import jwt
from datetime import datetime, timedelta
from typing import Optional
from bcrypt import hashpw, checkpw, gensalt
from app.config import get_settings

settings = get_settings()

def hash_password(password: str) -> str:
    """Genera hash de contraseña con bcrypt"""
    salt = gensalt()
    return hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verifica contraseña contra hash"""
    return checkpw(password.encode(), hashed.encode())

def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Crea JWT token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.algorithm)
    return encoded_jwt

def decode_token(token: str) -> Optional[int]:
    """Decodifica JWT token y retorna user_id"""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.algorithm])
        user_id = int(payload.get("sub"))
        return user_id
    except:
        return None
