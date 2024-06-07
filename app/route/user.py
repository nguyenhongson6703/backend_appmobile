from fastapi import APIRouter, status , Depends, HTTPException
from .. import schema, database, utils, models, oauth2
from sqlalchemy.orm import Session
from datetime import datetime
router = APIRouter(
    prefix="/users"

)
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def  create_users(user: schema.UserCreate, db:Session = Depends(database.get_db)):
    new_pass = utils.hash(user.password)
    user.password = new_pass
    birthday: datetime
    if(user.birthday != None):
        birthday = datetime.utcfromtimestamp(user.birthday)
        
    else:
        birthday = None
    
    new_user = models.User(username = user.username, password = new_pass, birthday = birthday ,
                           email = user.email, phone = user.phone)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return new_user

@router.get("/getinfo", response_model=schema.UserOut)
def get_one_user(db: Session = Depends(database.get_db), user_current: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_current.id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Don't have any information")
    
    return user

@router.put("/updatepassword")
def update_password(user_update: schema.UserUpdatePassword, db:Session = Depends(database.get_db),
                    current_user : int = Depends(oauth2.get_current_user)):
    
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Don't have any information")
    new_pass = utils.hash(user_update.password)
    user_update.password = new_pass
    user_query.update(user_update.dict(), synchronize_session=False)
    db.commit()
    return {
        "message": "Update password sucessfully!"
    }
@router.put("/updateinfo", response_model=schema.UserOut)
def update_info(user_update:schema.UserUpdateInfo, db:Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Don't have any information")
    birthday: datetime
    if(user_update.birthday != None):
        birthday = datetime.utcfromtimestamp(user_update.birthday)
    else: 
        birthday = None
    update = {
        "birthday": birthday, 
        "email": user_update.email, 
        "phone": user_update.phone, 
    }
    user_query.update(update, synchronize_session=False)
    db.commit()
    return user_query.first()
