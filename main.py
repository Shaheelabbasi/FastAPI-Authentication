from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from Routes.route import router
from Routes.products import productRouter
app=FastAPI()
app.include_router(router)
app.include_router(productRouter)





# suppose we have to send a big data containing more than one field
# we will use know pydantic