from click import prompt
from sqlalchemy.orm import Session
from fastapi import APIRouter
from ....schemas.video import GeneralVideoFormat, videoCreate
from ....schemas.user import SessionUser
from fastapi import Depends
from ....db.database import get_session_db
from ....models.video import VideoModel
from ....models.user import UserModel
from ....core.security import get_current_user_from_session

router = APIRouter()


@router.get("/all")
async def get_all_videos(
    db : Session = Depends(get_session_db)

) -> list[GeneralVideoFormat] | None:
    
    _videos = db.query(VideoModel).all()

    videos = [GeneralVideoFormat.model_validate(video) for video in _videos]
    
    return videos


@router.post('/create')
async def create_video(
    video_create : videoCreate,
    user : SessionUser = Depends(get_current_user_from_session),
    db : Session = Depends(get_session_db)
):
    
    user = db.query(UserModel).filter(UserModel.username == user.username).first()
    _video = VideoModel(
        prompt = video_create.prompt,
        type = video_create.type,
        status= 'sendToService',
        owner_id = user.user_id,
    )
    
    db.add(_video)
    db.commit()
    db.refresh(_video)

    return GeneralVideoFormat.model_validate(_video)
    
    