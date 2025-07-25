from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from models import User
from dependencies import get_current_user
from dtos.auth import LoginInput, LoginOutput, ChangePasswordInput, ChangePasswordOutput, ChangeUsernameInput, ChangeUsernameOutput
from dtos.users import UserOutput
from services.auth import encode_token
from services.users import change_password, change_username

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
async def login(input: LoginInput, session: Session = Depends(get_session)):
    success, data = encode_token(session, input.username, input.password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return LoginOutput(access_token=data, token_type="bearer")

@router.patch("/change-password")
async def changePassword(input: ChangePasswordInput, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = change_password(session, current_user, input.current_password, input.new_password, input.confirm_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return ChangePasswordOutput(message=data)

@router.patch("/change-username")
async def changeUsername(input: ChangeUsernameInput, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success1, data1 = change_username(session, current_user, input.new_username, input.password)
    if not success1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data1,
            headers={"WWW-Authenticate": "Bearer"},
        )
    success2, data2 = encode_token(session, input.new_username, input.password)
    return ChangeUsernameOutput(message=data1, access_token=data2)



@router.get("/me")
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserOutput(current_user)