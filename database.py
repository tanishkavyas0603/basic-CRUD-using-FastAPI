from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_url=os.getenv["DataBase URL"]
engine= create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
