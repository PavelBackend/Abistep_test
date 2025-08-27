from fastapi import APIRouter, Depends
from api.database import get_async_session
from api.depends import get_payment_service
from api.internal.models.payment import TransferRequest, TransferResponse
from api.internal.services.payment import PaymentService


router = APIRouter(prefix='/payment')


@router.post("/transfer", response_model=TransferResponse, status_code=200)
async def transfer(
    transfer_data: TransferRequest,
    payment_service: PaymentService = Depends(get_payment_service),
    session=Depends(get_async_session)
):
    return await payment_service.tranfer(transfer_data=transfer_data, session=session)