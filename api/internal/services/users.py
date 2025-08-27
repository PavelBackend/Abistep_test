from fastapi import HTTPException
from api.internal.models.users import UserCreateRequest, UserModel, UsersResponse
from api.internal.repository.users import UsersRepo
from sqlalchemy.ext.asyncio import AsyncSession


class UsersService:
    def __init__(
        self,
        payment_service: "PaymentService",
        users_repo: UsersRepo
    ):
        self.payment_service = payment_service
        self.users_repo = users_repo

    @classmethod
    async def get_service(cls, payment_service = None) -> "UsersService":
        if payment_service:
            from api.internal.services.payment import PaymentService
            payment_service = await PaymentService.get_service()
        return cls(payment_service=payment_service, users_repo=UsersRepo())
    
    async def get_user_by_id(self, user_id: int, session: AsyncSession):
        return await self.users_repo.get_user_by_id(user_id=user_id, session=session)
    
    async def create_user(self, user_model: UserCreateRequest, session: AsyncSession) -> UserModel:
        if await self.users_repo.email_exists(email=user_model.email, session=session):
                raise HTTPException(400, "Данный email уже используется!")
        
        try:
            new_user = await self.users_repo.create_user(user_model=user_model, session=session)
            await session.commit()
            await session.refresh(new_user)

            return UserModel.model_validate(new_user, from_attributes=True)
        except Exception as e:
            await session.rollback()
            raise HTTPException(500, f"Ошибка при создании пользователя: {e}")
        
    async def get_all_users(self, session: AsyncSession) -> UsersResponse:
        try:
            all_users = await self.users_repo.get_all_users(session=session)
            return UsersResponse(
                users=[UserModel.model_validate(user, from_attributes=True) for user in all_users]
            )
        except Exception as e:
            raise HTTPException(500, f"Ошибка при получении всех пользователей: {e}")