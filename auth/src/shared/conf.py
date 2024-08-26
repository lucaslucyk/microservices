from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # mongo
    MONGO_MIN_POOL_SIZE: int = Field(default=10)
    MONGO_MAX_POOL_SIZE: int = Field(default=50)
    # miliseconds
    MONGO_MAX_IDLE_TIME: int = Field(default=10000)
    MONGO_CONNECT_TIMEOUT: int = Field(default=10000)
    MONGO_WAIT_QUEUE_TIMEOUT: int = Field(default=10000)
    MONGO_SERVER_SELECTION_TIMEOUT: int = Field(default=10000)


settings = Settings()
