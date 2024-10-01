from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER = 'postgres'
PASSWORD = 'postgres'
HOST ='localhost'
PORT = '5432'
DATABASE = 'loja'

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(USER,PASSWORD,HOST,PORT,DATABASE)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependência
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
