from api.internal.services.payment import PaymentService
from api.internal.services.users import UsersService


async def get_users_service() -> UsersService:
    return await UsersService.get_service()

async def get_payment_service() -> PaymentService:
    return await PaymentService.get_service()