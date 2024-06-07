from fastapi import Response, status, HTTPException, Depends , APIRouter
from typing import List, Optional
from .. import models, schema, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix= "/courses"
)
@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[schema.CourseDetail])
def get_all_course(db: Session = Depends(get_db)):
     courses = db.query(models.Course, models.User.username).join(models.User, models.User.id == models.Course.user_id).all()
    
    # Transform the query result into the schema you want to return
     courses_with_username = [{
        "id": course.id,
        "name": course.name,
        "start_date": course.start_date,
        "end_date": course.end_date,
        "description": course.description,
        "quantity_words": course.quantity_words,
        "username": username
    } for course, username in courses]
    
     return courses_with_username

@router.post("/participate", status_code=status.HTTP_201_CREATED, response_model=schema.ParticipateResponse)
def participate_course( course_create: schema.ParticipateCreate, db: Session = Depends(get_db), user_current : int = Depends(oauth2.get_current_user)):


    if(db.query(models.Participate).filter_by(user_id = user_current.id , course_id = course_create.course_id ).first()):
         raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"You had participated the course")
    course = db.query(models.Course).filter(models.Course.id == course_create.course_id).first()
    new_participate = models.Participate(
          
          user_id = user_current.id,
          course_id = course.id,
          leared_word = 0,
          not_leared_word = course.quantity_words,
          percent_completed = 0,
    ) 
    

    db.add(new_participate)
    
    

     # Lấy danh sách các từ vựng có course_id tương ứng
    vocabulary_list = db.query(models.Vocabulary).filter(models.Vocabulary.course_id  == course.id).all()

     # Lấy danh sách các tracking records
    tracking_records = []
    for vocab in vocabulary_list:
          tracking_record = models.Tracking(user_id=user_current.id, vocabulary_id=vocab.id, score=0)
          tracking_records.append(tracking_record)

     # Thêm các tracking records vào session
    db.add_all(tracking_records)

     
    db.commit()
    
    db.refresh(new_participate)

    return new_participate     

@router.get("/get_course_participate", status_code= status.HTTP_200_OK, response_model=  List[schema.CourseParticipated])
def get_course_participated(db: Session = Depends(get_db), user_current : int = Depends(oauth2.get_current_user)):
     # Thực hiện truy vấn để lấy các dữ liệu cần thiết từ các bảng Participate và Course
     query = db.query(
     models.Participate.percent_completed,
     models.Participate.leared_word,
     models.Participate.course_id,
     models.Course.name,
     models.Course.start_date,
     models.Course.quantity_words
     ).join(
     models.Course, models.Participate.course_id == models.Course.id
     ).filter(
     models.Participate.user_id == user_current.id
     )

     # Thực hiện lấy kết quả từ truy vấn
     result = query.all()
     return result



@router.post("/createcourse", status_code=status.HTTP_201_CREATED, response_model=schema.Course)
def create_course(course: schema.CourseCreate, db: Session = Depends(get_db), user_current : int = Depends(oauth2.get_current_user)):
     
     start_date : datetime
     end_date:datetime
     if(course.start_date != None):
          start_date = datetime.utcfromtimestamp(course.start_date)
     else:
          start_date = datetime.now()

     if(course.end_date != None):
          end_date = datetime.utcfromtimestamp(course.end_date)
     else:
          end_date = None
     new_course = models.Course(user_id = user_current.id, name = course.name, start_date = start_date, end_date = end_date, description = course.description,
                                quantity_words = course.quantity_words)
     db.add(new_course)
     db.commit()
     db.refresh(new_course)

     return new_course

@router.get("/getcourse/{id}", response_model=schema.Course)
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The course has id: {id} was not found")
    
    return course
@router.put("/updatecourse/{id}", response_model=schema.Course)
def update_course(id:int , course_update:schema.CourseCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The course has {id} is not found")
    if course.user_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not authorized to perform requested action")
    start_date : datetime
    end_date:datetime
    if(course_update.start_date != None):
          start_date = datetime.utcfromtimestamp(course_update.start_date)
    else:
          start_date = datetime.now()

    if(course_update.end_date != None):
          end_date = datetime.utcfromtimestamp(course_update.end_date)
    else:
          end_date = None
   
    update_course = {
        "name" : course_update.name, 
        "start_date": start_date, 
        "end_date": end_date, 
        "description": course_update.description, 
        "quantity_words": course_update.quantity_words
    }
    course_query.update(update_course, synchronize_session=False)
    db.commit()
    return course_query.first()
@router.delete("/deletecourse/{id}")
def delete_course(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
     return {
          "message": "Delete successfully"
     }
