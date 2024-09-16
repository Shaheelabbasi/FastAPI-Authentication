from pydantic import BaseModel,Field,constr

# userModel for database 
class Users(BaseModel):
    username:str
    email:str
    password:str=Field(...,min_length=6)

    
class Login(BaseModel):
    username:str
    password:str

    # models for adding the fields to the database 