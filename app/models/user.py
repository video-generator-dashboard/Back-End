from ..db.database import Base
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Enum as SQLEnum
from .video import VideoModel

class UserModel(Base):

    __tablename__ = "users_table"


    user_id : Mapped[int] = mapped_column(primary_key=True, index=True)
    username : Mapped[str] = mapped_column(index=True)
    password : Mapped[str] = mapped_column(index=True)

    videos = relationship(
        'VideoModel', back_populates='owner', cascade='all, delete-orphan'
    )






