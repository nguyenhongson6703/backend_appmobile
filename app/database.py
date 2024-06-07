from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_username = "postgres"
db_password = "son06072003"
db_host = "localhost"
db_name = "app_mobile"

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_username}:{db_password}@{db_host}/{db_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()