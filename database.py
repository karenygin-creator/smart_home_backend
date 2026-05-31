from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL="postgresql://postgres:Admin@localhost/smart_home"
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autoflush=False, bind=engine)
Base=declarative_base()