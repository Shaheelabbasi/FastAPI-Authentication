import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from Routes.products import oauth2_scheme
from Config.database import collectionname
pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

def generate_access_Token(data:dict,expires_In:timedelta):
    to_encode=data.copy()
    token_expiry=datetime.now()+expires_In
    to_encode.update({"exp":token_expiry})
    token=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print(jwt.ExpiredSignatureError)
        return None
    except jwt.InvalidTokenError:
        return None   
    

    # checks the validity of the token and ensures that the user exists in the database 
    # and hasn't been deactivated, deleted, or altered.
    #his provides a more secure and reliable way to work with authenticated users.
async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)]):
       
       payload=verify_token(token)
       if not payload:
           raise HTTPException(
               status_code=400,
               detail="Invalid Token"   
           )
    #    getting the user id from the payload
       user_id=payload.get("_id")
       user=collectionname.find_one({"id":user_id})
       if not user:
           raise HTTPException(
               400,
               detail="user not found"
           )
       return user
       

    

