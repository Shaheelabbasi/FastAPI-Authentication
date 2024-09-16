from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import APIRouter,Depends
productRouter=APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@productRouter.get("/products")
def getProducts(token:Annotated[str,Depends(oauth2_scheme)]):
    from Utils.auth_utils import verify_token
    paylod=  verify_token(token)
    if(paylod):
        return{"protected route accesseed"}
    # return {"token":token}