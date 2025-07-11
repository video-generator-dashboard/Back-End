from ..db.database import Base
from enum import Enum
from datetime import date, datetime
from sqlalchemy import Integer, DateTime, ForeignKey, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship, mapped_column, Mapped

class Video_Status(Enum):
    generating = 'GENERATING'
    readyToPublish = 'READYTOPUBLISH'
    published = 'PUBLISHED'
    denided = 'DENIDED'
    sendToService = 'SENDTOSERVICE'

class Video_Type(Enum):
    games = 'GAME'
    bio = 'BIOLOGY'
    hist = 'HISTORY'
    health = 'HEALTH'
    lifesHack = 'Lifes Hack'
    sport = 'SPORT'
    none = 'LISTOUT'

class VideoModel(Base):

    __tablename__ = 'videos_table'

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True,nullable=False)
    title : Mapped[str] = mapped_column(String(255), index=True,nullable=True)
    status : Mapped[str] = mapped_column(
        String(20),
        default=Video_Status.sendToService,nullable=True)
    type : Mapped[str] = mapped_column(
        String(20),
        default=Video_Type.none,nullable=True)
    last_updated : Mapped[date] = mapped_column(default=datetime.now(), nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),default=datetime.now, nullable=True)
    prompt : Mapped[str] = mapped_column(Text, nullable=True)

    output_url : Mapped[str] = mapped_column(String(500), nullable=True)
    thumbnail_url : Mapped[str] = mapped_column(String(500), nullable=True)

    task_id : Mapped[str] = mapped_column(String(255), nullable=True) #eğer celery de kuyruğa girerse iD'si burda saklancak
    processing_message: Mapped[str] = mapped_column(Text, nullable=True) #işlem sırasında verilen hatalar veya bildirimler

    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=True)
    owner_id : Mapped[int] = mapped_column(ForeignKey('users_table.user_id'), nullable=False)
    owner = relationship('UserModel', back_populates='videos')
    #UserModel 'i model olarak verilir back_populates ise diğer tablodaki tutulan değerlere referasndır
    #yani User da videos adında bir tablo olmalı.
    
    video_history : Mapped[str] = mapped_column(Text, nullable=True)