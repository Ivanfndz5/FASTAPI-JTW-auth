from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from app.models.user import User
from app.core.security import create_access_token
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')


def verify_password(plain_password: str, hashed_password : str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: str, password: str, db: Session= Depends(get_db)):
    '''
    busca el usuario por email
    verifica password hasheada
    si todo esta listo genera JWT
    '''
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password,user.hashed_password):
        return None

    access_token = create_access_token(
        user_id=str(user.id),
        role = user.role
    )
    return access_token