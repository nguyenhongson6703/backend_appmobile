from fastapi import Response , status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import models, schema,oauth2
from sqlalchemy.orm import Session
from ..database import get_db
import random

router = APIRouter(
    prefix="/vocabulary"
)
@router.post("/create", response_model=schema.Vocabulary)
def create_vocabulary(vocabulary: schema.VocabularyCreate, db:Session = Depends(get_db), user_current : int = Depends(oauth2.get_current_user)):
    new_vocabulary = models.Vocabulary(**vocabulary.dict())
    db.add(new_vocabulary)
    db.commit()
    db.refresh(new_vocabulary)

    return new_vocabulary
@router.put("/updatevocabulary/{id}", response_model=schema.Vocabulary)
def update_vocabulary(id:int, vocabulary_update: schema.VocabularyCreate, db:Session = Depends(get_db), user_current: int = Depends(oauth2.get_current_user)):
    vocabulary_query = db.query(models.Vocabulary).filter(models.Vocabulary.id == id)
    vocabulary = vocabulary_query.first()
    if vocabulary == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"The post has id : {id} has not found"
                            )
    course_id = vocabulary.course_id
    belong_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if belong_course.user_id != user_current.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=" Not authorized to perform requested action")
    try:

        vocabulary_query.update(vocabulary_update.dict(), synchronize_session=False)
    except Exception as e:
        print(e)
    db.commit()
    return vocabulary_query.first()

@router.put("/upload_image", response_model=schema.Vocabulary)
def update_vocabulary(image: schema.Image, db:Session = Depends(get_db)):
    vocabulary_query = db.query(models.Vocabulary).filter(models.Vocabulary.id == image.id_vocabulary)
    vocabulary = vocabulary_query.first()
    if vocabulary == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail=f"The post has id : {id} has not found"
                            )
    vocabulary.image_url = image.image_url
    
    db.commit()
    db.refresh(vocabulary)
    return vocabulary


@router.get("/{id}", response_model=schema.Vocabulary)
def get_vocabulary(id: int , db: Session = Depends(get_db), user_current: int = Depends(oauth2.get_current_user)):
    vocabulary = db.query(models.Vocabulary).filter(models.Vocabulary.id == id).first()
    if vocabulary == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"The vocabulary has {id} has not found")
    return vocabulary

@router.get("/belongcourse/{id}", response_model=List[schema.Vocabulary])
def get_vocabulary_by_course_id(id:int , db:Session = Depends(get_db), user_current : int = Depends(oauth2.get_current_user)):
    vocabularies = db.query(models.Vocabulary).filter(models.Vocabulary.course_id == id).all()
    if vocabularies == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"The vocabulary has {id} has not found")
    return vocabularies

@router.get("/review/{id}", response_model=List[schema.Vocabulary])
def get_vocabulary_by_course_id(id: int , db:Session = Depends(get_db), user_current : int = Depends(oauth2.get_current_user)):
    vocabularies = db.query(models.Vocabulary).filter(models.Vocabulary.course_id == id).all()

    if vocabularies == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"The vocabulary has {id} has not found")
    
    random_vocabularies = random.sample(vocabularies,4)
    return random_vocabularies
@router.get("/new_word/{id}", response_model=schema.Vocabulary)
def get_vocabulary_by_course_id(id: int , db:Session = Depends(get_db), user_current : int = Depends(oauth2.get_current_user)):
    vocabularies = db.query(models.Vocabulary).filter(models.Vocabulary.course_id == id).all()

    if vocabularies == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"The vocabulary has {id} has not found")
    
    random_vocabulary = random.choice(vocabularies)
    return random_vocabulary
@router.put("/score",status_code= status.HTTP_200_OK, response_model=schema.Tracking)
def get_vocabulary_by_course_id(score: schema.Score, db:Session = Depends(get_db), user_current : int = Depends(oauth2.get_current_user)):
     # Fetch the tracking entry
    tracking_query = db.query(models.Tracking).filter(models.Tracking.user_id == user_current.id, models.Tracking.vocabulary_id == score.id_vocabulary)
    tracking = tracking_query.first()
    if not tracking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tracking entry not found")
    # Update the score
    if(tracking.score <= 20):
        tracking.score += 2
        db.commit()
        db.refresh(tracking)
        # Check if score is greater than 20
        if tracking.score > 20:
            participate_query = db.query(models.Participate).filter(models.Participate.user_id == user_current.id, models.Participate.course_id == score.id_course)
            participate = participate_query.first()

            if not participate:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Participation entry not found")

            # Update participate entry
            participate.leared_word += 1
            participate.not_leared_word -= 1
            total_words = participate.leared_word + participate.not_leared_word
            if total_words > 0:
                participate.percent_completed = (participate.leared_word / total_words) * 100
            else:
                participate.percent_completed = 0.0

            db.commit()
            db.refresh(participate)

    return tracking


@router.delete("/deletevocabulary/{id}")
def delete_vocabulary(id:int, db:Session = Depends(get_db), user_current : int = Depends(oauth2.get_current_user)):
    return {
        "message": "Delete vocabulary successfully"
    }