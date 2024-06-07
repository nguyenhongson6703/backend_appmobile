from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import database, models
from fastapi import HTTPException, status
oath2_schema =  OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt
def verify_access_token(token: str , credentials_exception):
    try:
        payload = jwt.decode(token=token, key = SECRET_KEY, algorithms= [ALGORITHM])
        id: int = int(payload.get("user_id"))
        if id is None:
            raise credentials_exception
    except JWTError as j:
        print(j)
        raise credentials_exception
    return id

def get_current_user(token:str = Depends(oath2_schema), db: Session = Depends(database.get_db)):


    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers=
                                          {"WWW-Authenticate": "Bearer"}  )
    token = verify_access_token(token=token , credentials_exception= credentials_exception)
    user = db.query(models.User).filter( models.User.id == token).first()

    return user
