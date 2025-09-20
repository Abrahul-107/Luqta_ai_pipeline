from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import create_access_token, verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

user_db = {
    "rahul": {"username": "rahul", "password": "rahul@luqtaai#pipeline"}
}

class AuthService:
    def authenticate_user(self, username: str, password: str):
        user = user_db.get(username)
        if not user or user["password"] != password:
            return None
        return user

    def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # Added access_token_expires to the response
        access_token_expires = timedelta(minutes=60)
        token = create_access_token({"sub": user["username"]}, expires_delta=access_token_expires)
        return {"access_token": token, "token_type": "bearer", "access_token_expires_in_minutes": access_token_expires/60}

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        username = verify_token(token)
        if username is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
        return username
