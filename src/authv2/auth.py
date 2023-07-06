
from datetime import datetime, timedelta
from typing import Union

from fastapi import HTTPException,Response
from fastapi import Depends
from passlib.hash import scrypt,bcrypt
from sqlalchemy import  select
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from config import SECRET, JWT_LIFE
from utils.database import get_async_session
from src.authv2.schemas import Token, UserRead, CreateUser, User_Change_Email, AnonymousUserRead
from src.authv2.models import User

# oauth_schema = CustomOAuth2PasswordBearer(tokenUrl = '/auth/sign-in/')

async def get_current_user(request:Request)->UserRead:
    data = AuthService.validate(request)
    return data
async def get_current_user_or_pass(request:Request)->Union[UserRead,AnonymousUserRead]:
    try:
        data = AuthService.validate(request)
    except:
        data = AnonymousUserRead(
            id = -1,
            username = 'AnonymousUser'

        )
    return data


async def get_user_model(session:AsyncSession = Depends(get_async_session),
                         user:UserRead = Depends(get_current_user)) ->User:
    username = user.username
    query = select(User).where(User.username == username)
    user = (await session.execute(query)).scalars().first()
    return user

class AuthService:
    exception = HTTPException(
        status_code=401,
        detail='error',
    )
    def __init__(self,session:AsyncSession = Depends(get_async_session)):
        self.session = session
    async def register_new_user(self,user_data:CreateUser,response:Response)->Token:
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=self.hash_password(user_data.password)
        )
        self.session.add(user)
        await  self.session.commit()
        return  self.create_token(user,response)
    async def change_email(self,user_data:User_Change_Email,response:Response,request:Request ):
        old_user = self.validate(request)
        id_user = old_user.id
        print(id_user)
        query = select(User).where(User.id == id_user)
        user = (await self.session.execute(query)).scalars().first()
        is_Match = self.verify_password(user_data.password,user.hashed_password)
        print(is_Match)
        assert is_Match ,self.exception
        user.email = user_data.email
        self.session.add(user)
        await self.session.commit()
        return self.create_token(user,response)

    async def authenticate_user(self,username:str,password:str,response:Response,start)->Token:
        query = select(User).where(User.username == username)
        user = (await self.session.execute(query)).scalars().first()


        exception = HTTPException(
            status_code=401,
            detail='Couldt validate data',
            headers={'Authorization': 'Bearer'}
        )
        if not user:
            raise exception
        if not self.verify_password(password,user.hashed_password):
            raise exception
        return self.create_token(user,response)
    @classmethod
    def verify_password(cls,raw_password:str,hash_password:str):
        print( hash_password[0])
        if hash_password[0] == '$':
            return bcrypt.verify(raw_password,hash_password)
        return scrypt.verify(raw_password,hash_password)
    @classmethod
    def hash_password(cls,password:str)->str:
        return scrypt.hash(password)
    @classmethod
    def validate(cls,request:Union[Request,str])->UserRead:
        access_token = request
        if isinstance(request,Request):
            access_token = request.cookies.get('access_token')
        exception = HTTPException(
            status_code=401,
            detail='Could not  validate data'
        )
        if not access_token:
            raise exception
        token = access_token.split(' ')[1].rstrip()

        payload = jwt.decode(token,SECRET,algorithms=['HS256'],verify=True)
        user_data = payload.get("user")
        try:
            user = UserRead.parse_obj(user_data)
        except:
            raise exception
        return user

    @classmethod
    def validate_grpc(cls, access_token: str) -> UserRead:
        exception = HTTPException(
            status_code=401,
            detail='Could not  validate data'
        )
        if not access_token:
            raise exception
        token = access_token.split(' ')[1].rstrip()

        payload = jwt.decode(token, SECRET, algorithms=['HS256'], verify=True)
        user_data = payload.get("user")
        try:
            user = UserRead.parse_obj(user_data)
        except:
            raise exception
        return user
    @classmethod
    def create_token(cls,user:User,response:Response)->Token:
        user_data =   jsonable_encoder(UserRead.from_orm(user))
        now = datetime.utcnow()
        payload = {
            "iat":now,
            'nbf':now,
            'exp':now + timedelta(seconds=JWT_LIFE),
            'sub':str(user_data['id']),
            'user':user_data

        }
        token = jwt.encode(
            payload,
            SECRET,
            algorithm='HS256'
        )
        response.set_cookie('access_token',"Bearer "+token,expires = JWT_LIFE)
        return Token(access_token = token)
