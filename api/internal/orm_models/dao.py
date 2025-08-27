from sqlalchemy import Integer, String, ForeignKey, Boolean, TIMESTAMP, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
from decimal import Decimal


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    sent_transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="sender",
        foreign_keys="Transaction.sender_id",
        cascade="all, delete-orphan"
    )

    received_transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="receiver",
        foreign_keys="Transaction.receiver_id",
        cascade="all, delete-orphan"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    sender_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    receiver_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
    )
    paid_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    sender: Mapped["Users"] = relationship(
        "Users",
        back_populates="sent_transactions",
        foreign_keys=[sender_id],
    )

    receiver: Mapped["Users"] = relationship(
        "Users",
        back_populates="received_transactions",
        foreign_keys=[receiver_id],
    )
