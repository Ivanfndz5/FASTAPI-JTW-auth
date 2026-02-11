from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from passlib.context import CryptContext
from app.core.security import get_current_user,require_role

router = APIRouter(prefix='/users', tags=['users'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/', response_model=UserRead)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # hasheamos la contraseña
    hashed = pwd_context.hash(user_in.password)

    user = User(
        email=user_in.email,
        hashed_password=hashed,
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post('/', response_model=UserRead)
def create_user(user_in:UserCreate, db: Session = Depends(get_db)):
    #hasheamos la contraseña
    hashed = pwd_context.hash(user_in.password)

    user = User(
        email=user_in.email,
        hashed_password=hashed,
        role=user_in.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=UserRead)
def read_current_user(
        token_data: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user_id = token_data["user_id"]
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user



@router.get("/vip-data")
def vip_data(token_data: dict = Depends(require_role("VIP"))):
    return {"message": f"Hola VIP {token_data['user_id']}"}


