from fastapi import APIRouter, Depends, HTTPException, status
from .. import schema , database, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
router = APIRouter(
    tags=["authentication"]
)
@router.post("/login", response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credential")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credential")
    
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }