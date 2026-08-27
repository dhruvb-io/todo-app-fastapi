import os
from dotenv import load_dotenv
from urllib.parse import quote
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)

metadata = MetaData()

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()