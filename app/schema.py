from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password:str
    birthday: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
class UserOut(BaseModel):
    id:int
    username: str
    birthday: Optional[datetime] = None
    email:Optional[str] = None
    phone: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserUpdatePassword(BaseModel):
    username: str 
    password: str

class UserUpdateInfo(BaseModel):
    email: str = None
    phone: str = None
    birthday: int = None

class Course(BaseModel):
    id: int
    name :str
    start_date : Optional[datetime] = None 
    end_date: Optional[datetime] = None
    description : str
    quantity_words: int
class CourseDetail(BaseModel):
    id: int
    name :str
    start_date : Optional[datetime] = None 
    end_date: Optional[datetime] = None
    description : str
    quantity_words: int
    username: str

class CourseCreate(BaseModel):
    name: str
    start_date: Optional[int] = None
    end_date: Optional[int] = None
    description: str
    quantity_words: int

class ParticipateCreate(BaseModel):
    course_id : int

class ParticipateResponse(BaseModel):
    id : int
    user_id :int 
    course_id : int
    created_at : Optional[datetime]
    leared_word : int
    not_leared_word  :int
    percent_completed : float
   
class CourseParticipated(BaseModel):
    percent_completed: float 
    leared_word: int
    course_id: int
    name: str
    start_date: datetime
    quantity_words: int
class VocabularyCreate(BaseModel):
    
    english : str
    vietnamese :str
    spell : Optional[str] = None
    parts_of_speech : str
    mp3_url : Optional[str] = None
    image_url : Optional[str] = None
    course_id : int 
    example : Optional[str] = None
    example_translate : Optional[str] = None
class Vocabulary(BaseModel):
    id: int
    english : str
    vietnamese :str
    spell : Optional[str] = None
    parts_of_speech : str
    mp3_url : Optional[str] = None
    image_url : Optional[str] = None
    course_id : int 
    example : Optional[str] = None
    example_translate : Optional[str] = None
class Image(BaseModel):
    image_url: str
    id_vocabulary:int

class Score(BaseModel):
    id_course: int
    id_vocabulary: int
class Tracking(BaseModel):
    id :int
    user_id :int
    vocabulary_id : int
    score : int
    
    
