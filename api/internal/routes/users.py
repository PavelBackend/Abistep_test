from fastapi import APIRouter, Depends
from api.database import get_async_session
from api.depends import get_users_service
from api.internal.models.users import UserCreateRequest, UsersResponse, UserModel
from api.internal.services.users import UsersService

router = APIRouter(prefix='/users')

@router.post("/", response_model=UserModel, status_code=201)
async def create_user(
    user: UserCreateRequest,
    users_service: UsersService = Depends(get_users_service),
    session=Depends(get_async_session),
):
    return await users_service.create_user(user_model=user, session=session)

@router.get('/', response_model=UsersResponse, status_code=200)
async def get_users(
    users_service: UsersService = Depends(get_users_service),
    session=Depends(get_async_session)
):
    return await users_service.get_all_users(session=session)