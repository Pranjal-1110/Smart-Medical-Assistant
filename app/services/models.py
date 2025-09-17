from pydantic import BaseModel , EmailStr
class UserRegister(BaseModel):
    first_name: str
    last_name: str
    username : str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username_or_email : str
    password: str

class VerificationDetails(BaseModel):
    license_number: str