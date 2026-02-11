from fastapi import APIRouter,HTTPException
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import authenticate_user

router = APIRouter(prefix='/auth',tags=['auth'])

@router.post('/login', response_model=TokenResponse)
def login(data: LoginRequest):
    '''
    Endpoint para login de usuario
    Valida credenciales, y devuelve un JWT
    '''
    token = authenticate_user(data.email, data.password)
    if not token:
        raise HTTPException(
            status_code=401,
            detail='Invalid credentials'
        )
    return {'access_token': token}