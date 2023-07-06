import datetime
from datetime import time

from fastapi import APIRouter, Depends,Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from src.authv2.schemas import CreateUser,Token,UserRead,User_Change_Email
from src.authv2.auth import AuthService,get_current_user
router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

@router.post('/register',response_model= Token)
async def login(response:Response,user_data:CreateUser,service:AuthService = Depends()):
    return await service.register_new_user(user_data,response)

@router.post('/login',response_model= Token)
async def login(
        response:Response,
        user_data:OAuth2PasswordRequestForm = Depends(),
        service:AuthService = Depends()
):
    start =  datetime.datetime.now()
    return await service.authenticate_user(user_data.username,user_data.password,response,start)

@router.get('/get',response_model=UserRead)
async def get_user(user:UserRead = Depends(get_current_user)):
    return user



@router.post('/change_email',response_model=Token)
async def change_email(user_email_change:User_Change_Email, response:Response,request:Request,service:AuthService = Depends()):
    return await service.change_email(user_email_change,response = response,request=request)

