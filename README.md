# FASTAPI JWT Auth

Proyecto demo de FastAPI con autenticación JWT y control de roles.

## Funcionalidades

- Crear usuario: `POST /users/`  
- Login y obtención de token JWT: `POST /auth/login`  
- Obtener info del usuario autenticado: `GET /users/me` 🔒  
- Endpoint solo para usuarios VIP: `GET /users/vip-data` 🔒  

> 🔒 Los endpoints marcados con candado requieren token JWT en Authorization.

## Tecnologías

- Python 3.x  
- FastAPI  
- SQLAlchemy  
- Pydantic  
- Passlib (hash de contraseñas)  
- JWT (PyJWT)




