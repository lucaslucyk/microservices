from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    username: str