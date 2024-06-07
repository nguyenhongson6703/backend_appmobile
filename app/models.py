from .database import Base
from sqlalchemy import  Column, Integer, String, Text, ForeignKey, Float, DateTime, func, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable= False)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    birthday = Column(DateTime(timezone=False), nullable=True)
    email = Column(String(150), nullable=True)
    phone = Column(String(150), nullable=True)


class Course(Base):
    __tablename__ = 'course'
    
    id = Column(Integer,  primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(150), nullable=False)
    start_date = Column(DateTime(timezone=False), nullable=True)
    end_date = Column(DateTime(timezone=False), nullable=True)
    description = Column(Text, nullable=False)
    quantity_words = Column(Integer, nullable=False, default=1)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User")

class Participate(Base):
    __tablename__ = 'participate'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    created_at = Column(DateTime(timezone=False), nullable=True, default=func.now())
    leared_word = Column(Integer, nullable=False)
    not_leared_word = Column(Integer, nullable=False)
    percent_completed = Column(Float, nullable=True)
    user = relationship("User")
    course = relationship("Course")

class Vocabulary(Base):
    __tablename__ = 'vocabulary'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    english = Column(String(150), nullable=False)
    vietnamese = Column(String(150), nullable=False)
    spell = Column(String(150), nullable=True)
    parts_of_speech = Column(String(150), nullable=False)
    mp3_url = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    example = Column(Text, nullable=True)
    example_translate = Column(Text, nullable=True)
    course = relationship("Course")

class Tracking(Base):
    __tablename__ = 'tracking'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    vocabulary_id = Column(Integer, ForeignKey('vocabulary.id'), nullable=False)
    score = Column(Integer, nullable=False, default=0)
    user = relationship("User")
    vocabulary = relationship("Vocabulary")

    __table_args__ = (
        UniqueConstraint('user_id', 'vocabulary_id'),
    )