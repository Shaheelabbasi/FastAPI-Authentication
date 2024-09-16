from fastapi import APIRouter,HTTPException,Response, status,Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from Models.users import Users
from Models.users import Login
from Config.database import collectionname
from Schemas.UserSchema import Userschema
from Utils.auth_utils import generate_access_Token,hash_password,verify_password
from datetime import datetime, timedelta
router=APIRouter()


@router.post("/signup")
async def Sign_Up(user:Users):
  existing_user=collectionname.find_one({"$or":[{"username":user.username},{"email":user.email}]})
  if existing_user:
     raise HTTPException(
        status_code=400,
        detail="user already exists"
     )
  hashed_password=hash_password(user.password)

  newuser=collectionname.insert_one({"username":user.username,"email":user.email,"password":hashed_password})
  created_user= collectionname.find_one({"_id":newuser.inserted_id})
# Ensure created_user is not None before trying to access it
  if created_user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return Userschema(
    username=created_user["username"],
    email=created_user["email"],
    message="account created successfully"
  )



@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    existing_user=collectionname.find_one({"$or":[{"username":form_data.username}]})
    if existing_user is None:
        return JSONResponse(
           content={"message":"user does not exist"},
           status_code=status.HTTP_400_BAD_REQUEST
        )
    loggedin_user=verify_password(form_data.password,existing_user["password"])
    if not loggedin_user:
        raise HTTPException(
           400,
           detail="incorrect password"
        )
    token= generate_access_Token({"_id":str(existing_user["_id"]),"username":existing_user["username"]},timedelta(minutes=40))
    print(token)
        
    return {
       "access_token": token,
        "token_type": "bearer"
    }
  