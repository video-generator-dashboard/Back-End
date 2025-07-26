import uuid

from ....core.security import get_password_hash, verify_password, get_current_user_from_session
from datetime import date, datetime, timedelta, timezone
from fastapi import Depends, HTTPException, APIRouter, status, Response, Request
from sqlalchemy.orm import Session

from ....db.database import get_session_db
from ....schemas.user import LoginUser, SessionUser, CreateUser, UpdateUser, UserAll
from ....models.user import UserModel
from ....models.session import SessionModel

router = APIRouter()

@router.post("/register", response_model=SessionUser, status_code = status.HTTP_201_CREATED)
async def register_user(
    user : CreateUser,
    db : Session = Depends(get_session_db)
):
    
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if db_user:
        raise HTTPException(status_code=400, detail='bu isimde kullanıcı var')
    
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        username = user.username,
        password = hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return SessionUser.model_validate(db_user)


@router.post('/login')
async def login_user(

    user : LoginUser,
    response: Response,
    db : Session = Depends(get_session_db)
):
    
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password) :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Geçersiz kimlik bilgileri")
    

    db.query(SessionModel).filter(SessionModel.user_id == db_user.user_id).delete() #eski oturumu sil
    db.commit()

    session_id = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)

    db_session = SessionModel(
        session_id = session_id,
        user_id = db_user.user_id,
        expires_at = expires_at
    )
    db.add(db_session)
    db.commit()

    #çerez işlemleri

    response.set_cookie(
        key='session_id',
        value=session_id,
        httponly=True,
        secure=True,
        samesite='LAX',
        expires = expires_at.strftime("%a, %d %b %Y %H:%M:%S GMT")
    )

    return {"message": "login okey"}

@router.post("/logout")
async def logout_user(
    request : Request,
    response : Response,
    db : Session = Depends(get_session_db)
):
    session_id = request.cookies.get('session_id')

    if session_id:
        db.query(SessionModel).filter(SessionModel.session_id == session_id).delete()
        db.commit()

    
    response.delete_cookie('session_id')
    return {'message' : 'logout okey'}


@router.get('/me')
async def read_current_user(
    current_user : SessionUser = Depends(get_current_user_from_session),
    db : Session = Depends(get_session_db)
) -> UserAll : 
    user = db.query(UserModel).filter(UserModel.username == current_user.username).first()
    return UserAll.model_validate(user)


@router.put('/updatepassword/{id}', status_code=status.HTTP_200_OK)
async def update_password(
    id : int,
    user_model : UpdateUser,
    db : Session = Depends(get_session_db)
):
    
    _user = db.query(UserModel).filter(UserModel.user_id == id).first()

    _user.password = get_password_hash(user_model.password)
    
    db.commit()
    db.refresh(_user)

    return {'message': 'Password updated successfully'}
