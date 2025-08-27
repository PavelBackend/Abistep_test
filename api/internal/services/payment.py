from decimal import Decimal
from fastapi import HTTPException
from api.internal.models.payment import TransferRequest, TransferResponse
from api.internal.models.users import BaseResponse
from api.internal.repository.payment import PaymentRepo
from api.internal.services.users import UsersService
from sqlalchemy.ext.asyncio import AsyncSession


class PaymentService:
    def __init__(
        self,
        users_service: UsersService,
        payment_repo: PaymentRepo
    ):
        self.users_service = users_service
        self.payment_repo = payment_repo

    @classmethod
    async def get_service(cls):
        users_service = await UsersService.get_service()
        return cls(users_service=users_service, payment_repo=PaymentRepo())
    
    async def check_enough_money(self, amount: Decimal, sender_balance: Decimal):
        return False if sender_balance < amount else True
    
    async def transfer(self, transfer_data: TransferRequest, session: AsyncSession) -> TransferResponse:
        if transfer_data.from_user_id == transfer_data.to_user_id:
            raise HTTPException(400, "Нельзя перевести деньги себе!")

        sender = await self.users_service.users_repo.get_user_by_id(
            user_id=transfer_data.from_user_id, session=session
        )
        if not sender:
            raise HTTPException(404, f"Отправитель с id {transfer_data.from_user_id} не найден")

        if not await self.check_enough_money(
            amount=transfer_data.amount, sender_balance=sender.balance
        ):
            raise HTTPException(400, "Недостаточно средств на счете")

        receiver = await self.users_service.users_repo.get_user_by_id(
            user_id=transfer_data.to_user_id, session=session
        )
        if not receiver:
            raise HTTPException(404, f"Получатель с id {transfer_data.to_user_id} не найден")

        try:
            await self.users_service.users_repo.pay(
                amount=transfer_data.amount, sender=sender, session=session
            )
            await self.users_service.users_repo.payout(
                amount=transfer_data.amount, receiver=receiver, session=session
            )
            await session.commit()

            return TransferResponse(
                sender_id=transfer_data.from_user_id,
                receiver_id=transfer_data.to_user_id,
                amount=transfer_data.amount,
                detail=f"Перевод от {transfer_data.from_user_id} к {transfer_data.to_user_id} выполнен"
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                500,
                f"Ошибка при переводе от {transfer_data.from_user_id} к {transfer_data.to_user_id}: {e}"
            )