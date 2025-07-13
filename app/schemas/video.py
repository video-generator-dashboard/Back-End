import datetime
from pydantic import BaseModel

class GeneralVideoFormat(BaseModel):

    id : int
    title : str | None
    status : str
    type : str
    last_updated : datetime.datetime
    created_at : datetime.datetime
    duration_seconds : int | None
    owner_id : int

    class Config:
        from_attributes = True


class videoCreate(BaseModel):
    prompt : str | None
    type : str | None

    class Config:
        from_attributes = True



class UpdateVideoFormat(BaseModel):

    id : int 
    title : int | None
    status : str | None
    type : str | None
    last_updated : datetime.datetime| None 
    created_at : datetime.datetime | None
    prompt : str | None

    output_url : str | None
    thumbnail_url : str | None

    task_id : str | None
    processing_message: str | None

    duration_seconds: int | None
    owner_id : int | None
    
    video_history : str | None

    class Config:
        from_attributes = True

class VideoDetailInfo(BaseModel):

    id : int 
    title : int | None
    status : str | None
    type : str | None
    last_updated : datetime.datetime | None 
    created_at : datetime.datetime | None
    prompt : str | None

    output_url : str | None
    thumbnail_url : str | None
    processing_message: str | None
    duration_seconds: int | None
    owner_id : int | None
    video_history : str | None

    class Config:
        from_attributes = True
