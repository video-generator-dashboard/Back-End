from datetime import datetime
from passlib.context import CryptContext
from fastapi import Depends, Request, status, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_session_db
from ..models.user import UserModel
from ..models.session import SessionModel
from ..schemas.user import SessionUser

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)



def get_current_user_from_session(
        request: Request,
        db : Session = Depends(get_session_db)
) -> SessionUser:
    
    session_id = request.cookies.get('session_id')

    if not session_id :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="oturum açılamadı")
    
    db_session = db.query(SessionModel).filter(
        SessionModel.session_id == session_id,
        SessionModel.expires_at > datetime.now()
    ).first() #süre kontrolü

    if not db_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Oturum süresi doldu")
    
    user = db.query(UserModel).get(db_session.user_id) #session sahibi

    if not user :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Kullanıcı bulunamadı")
    

    return SessionUser.model_validate(user) #SessionUser modeli donmesini istiyorum