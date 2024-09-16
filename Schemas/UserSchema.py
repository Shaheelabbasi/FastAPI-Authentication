from pydantic import BaseModel,Field
from typing import Optional
class Userschema(BaseModel):
    username:str
    email:str
    message:str
    token:Optional[str]=None
    
   