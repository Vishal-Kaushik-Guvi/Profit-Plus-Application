from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

# Password hashing setup
# In Java → new BCryptPasswordEncoder()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Password Functions ──────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Convert plain password to hashed password"""
    # In Java → passwordEncoder.encode(password)
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if entered password matches stored hash"""
    # In Java → passwordEncoder.matches(plain, hashed)
    return pwd_context.verify(plain_password, hashed_password)

# ── JWT Functions ───────────────────────────────────────────────────

def create_access_token(data: dict) -> str:
    """
    Create a JWT token with expiry
    In Java → Jwts.builder().setSubject(...).signWith(...).compact()
    """
    to_encode = data.copy()

    # Set expiry time
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    # Sign and create token
    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token

def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT token
    In Java → Jwts.parser().setSigningKey(...).parseClaimsJws(token)
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None