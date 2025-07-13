from csv import Error
from click import prompt
from sqlalchemy.orm import Session
from fastapi import APIRouter
from ....schemas.video import GeneralVideoFormat, UpdateVideoFormat, VideoDetailInfo, videoCreate
from ....schemas.user import SessionUser
from fastapi import Depends, HTTPException, status
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
    

@router.get('/recent')
async def recent_videos(
    db : Session = Depends(get_session_db)
) -> list[GeneralVideoFormat]:
    
    _videos = db.query(VideoModel).order_by(VideoModel.created_at.desc()).limit(4).all()

    videos = [GeneralVideoFormat.model_validate(video) for video in _videos]    

    return videos



@router.get("/{id}")
async def get_vide_with_id(
    id : int,
    db : Session = Depends(get_session_db)
) -> GeneralVideoFormat:
    
    video = db.query(VideoModel).filter(VideoModel.id == id).first()

    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="böyle bir video bulunamadı")
    
    return VideoDetailInfo.model_validate(video)


@router.put('/{id}')
async def update_video(
    id : int,
    video : UpdateVideoFormat,
    db : Session = Depends(get_session_db)
):
    
    return ""

    
