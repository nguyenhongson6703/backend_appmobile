from fastapi import FastAPI
from . import models
from .database import engine
from .route import user , auth, course, vocabulary




models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(course.router)
app.include_router(vocabulary.router)