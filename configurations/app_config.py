import os
from dotenv import load_dotenv
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


env_path = Path('../') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME:str = "Auth"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = os.getenv("POSTGRES_USER", "root")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "root")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5428)
    POSTGRES_DB : str = os.getenv("POSTGRES_DB","auth")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
    ALGORITHM = "HS256"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "SECRETKEYRANDOM1233401")
    JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY", "SECRETKEYRANDOM123") 

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


settings = Settings()
