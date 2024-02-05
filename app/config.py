from dotenv import load_dotenv
import os
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
    ALGORITHM = "HS256"
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']     # should be kept secret
    JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']      # should be kept secret
    MONGO_DB_URL = os.environ['MONGO_DB_URL']
    DATABASE_NAME = os.environ['DATABASE_NAME']
    MAX_POOL_SIZE = os.environ['MAX_POOL_SIZE']
    
settings = Settings()

