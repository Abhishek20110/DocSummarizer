import os
from datetime import datetime, timedelta
import bcrypt
import jwt
import logging

logger = logging.getLogger(__name__)
from fastapi import Request, HTTPException, status
from dotenv import load_dotenv

from .database import get_user_by_username

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Prevent errors if somehow already bytes
        password_bytes = plain_password.encode('utf-8') if isinstance(plain_password, str) else plain_password
        hash_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
        
        # bcrypt 4.0+ limits password lengths to 72 bytes
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
            
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except ValueError:
        return False

def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8') if isinstance(password, str) else password
    
    # bcrypt 4.0+ strictly enforces max length of 72 bytes
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request):
    """Dependency that checks if user is logged in via cookie and valid."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # If the token starts with Bearer, remove it. Usually for cookies we just store the token.
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
    except jwt.PyJWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user = await get_user_by_username(username)
    if user is None:
        logger.warning(f"Auth failed. User '{username}' not found in DB.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

async def get_current_user_optional(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            return None
    except jwt.PyJWTError:
        return None
    
    user = await get_user_by_username(username)
    return user

async def get_current_active_user(request: Request):
    user = await get_current_user(request)
    if not user.get("is_active", True):
        logger.warning(f"Access denied. User '{user.get('username')}' is inactive.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is not active. You cannot perform LLM actions."
        )
    
    return user
