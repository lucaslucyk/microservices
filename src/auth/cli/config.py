from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URI: str
    CRYPT_SCHEMAS: List[str] = ["bcrypt"]

    class Config:
        env_file = '.env'
        extra = 'ignore'

    
settings = Settings()