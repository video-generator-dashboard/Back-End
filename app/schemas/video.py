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