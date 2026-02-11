import jwt
from datetime import datetime,timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Decís dónde se obtiene el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extrae y valida el usuario actual desde el JWT.
    """
    try:
        payload = verify_token(token)  # usa tu función verify_token existente
        return payload  # {'user_id': ..., 'role': ...}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


# Secret y configuracion minimo

SECRET_KEY = "8f73a9b2c1e4d7f9a3e5b6c8d1f2a4e6"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(user_id: str, role:str, expires_delta: Optional[timedelta] = None):
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        'sub': user_id,
        'role' : role,
        'exp': expire

    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

#Funcion para verificar token y extraer usuario.

def verify_token(token : str):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        user_id : str = payload.get('sub')
        role : str = payload.get('role')
        if user_id is None or role is None:
            raise ValueError('Token invalido')
        return {'user_id': user_id, 'role': role}
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.PyJWTError:
        raise ValueError('Token invalido')


def require_role(required_role: str):
    def role_checked(token_data: dict = Depends(get_current_user)):
        user_role = token_data['role']
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail = 'Permiso denegado'
            )
        return token_data
    return role_checked

