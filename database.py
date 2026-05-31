from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL="postgresql+psycopg2://postgres:Admin@localhost/smart_home"
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autoflush=False, bind=engine)
Base=declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()