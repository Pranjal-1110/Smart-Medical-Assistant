from pydantic import BaseModel , EmailStr, Field
from typing import Optional, List

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
    
class DoctorResult(BaseModel):
    title: Optional[str] = Field(..., description="Title of the search result")
    name:str = Field(..., description="Name of the doctor")
    phone_number: Optional[str] = Field(..., description="Contact number of the doctor or clinic")
    address: str = Field(..., description="Address of the doctor or clinic")
    link : Optional[str] = Field(..., description="Link to the doctor's profile or clinic website")

class SearchOutput(BaseModel):
    results: list[DoctorResult] = Field(..., description="List of search results with name, phone number, and address. Optional link if available")