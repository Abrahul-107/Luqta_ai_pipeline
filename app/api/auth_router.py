from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post("/auth/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return auth_service.login(form_data)
