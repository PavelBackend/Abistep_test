from decimal import Decimal
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from api.internal.models.users import UserCreateRequest
from api.internal.orm_models.dao import Users

class UsersRepo:

    @staticmethod
    async def email_exists(email: str, session: AsyncSession):
        stmt = select(Users).where(Users.email == email)
        res = await session.execute(stmt)
        return res.scalars().first() is not None
    
    @staticmethod
    async def create_user(user_model: UserCreateRequest, session: AsyncSession) -> Users:
        new_user = Users(**user_model.model_dump())
        session.add(new_user)
        return new_user
    
    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[Users]:
        stmt = select(Users)
        result = await session.execute(stmt)
        return result.scalars().all()
    
    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> Users:
        stmt = select(Users).where(Users.id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def pay(amount: Decimal, sender: Users, session: AsyncSession):
        query = (
            update(Users)
            .where(Users.id == sender.id)
            .values(balance=Users.balance - amount)
        )
        await session.execute(query)

    @staticmethod
    async def payout(amount: Decimal, receiver: Users, session: AsyncSession):
        query = (
            update(Users)
            .where(Users.id == receiver.id)
            .values(balance=Users.balance + amount)
        )
        await session.execute(query)