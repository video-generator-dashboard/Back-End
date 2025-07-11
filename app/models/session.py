from ..db.database import Base
from datetime import  datetime, timedelta
from sqlalchemy import Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column, Mapped


class SessionModel(Base):
    __tablename__ = "sessions_table"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id : Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    user_id : Mapped[int] = mapped_column(ForeignKey("users_table.user_id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now() + timedelta(hours=7))

    user = relationship('UserModel')