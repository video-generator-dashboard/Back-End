from pydantic import BaseModel

#pydantic modelleri ve sqlalchmey modelleri birbirinden farklıdır ve kullanılmadan önce bir birilerine dönüştürülmeleri gerekir
class SessionUser(BaseModel):
    username : str | None

    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    username : str
    password : str

    class Config:
        from_attributes = True

class UpdateUser(BaseModel):
    username : str
    password : str

    class Config:
        from_attributes = True

class LoginUser(BaseModel):
    username : str
    password : str

    class Config:
        from_attributes = True

class UserAll(BaseModel):
    user_id : int
    username : str
    password : str
    
    class Config:
        from_attributes = True