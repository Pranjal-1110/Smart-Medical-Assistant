from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.auth.jwt_handler import create_access_token
from app.auth.oauth import oauth
from app.auth.dependencies import get_current_user
from app.services.mongodb import users_collection, doctor_licenses_collection, initialize_doctor_licenses
from app.services.password_hasher import get_password_hash, verify_password
from app.services.models import UserRegister, UserLogin, VerificationDetails
from bson import ObjectId
from starlette.config import Config 

config = Config(".env")

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default="15")

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/login/google")
async def login_via_google(request: Request):
    google = oauth.create_client("google")
    assert google is not None
    redirect_uri = request.url_for("auth_callback")
    return await google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request):
    client = oauth.create_client("google")
    assert client is not None
    token = await client.authorize_access_token(request)
    user_info = token.get("userinfo")
    
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not retrieve user info from Google."
        )

    user_email = user_info.get("email")

    existing_user = await users_collection.find_one({"email": user_email})
    
    if existing_user:
        user_id = str(existing_user["_id"])
        role = existing_user.get("role", "patient")
    else:
        new_user = {
            "google_id": user_info["sub"],
            "email": user_email,
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
            "role": "patient",
        }
        
        result = await users_collection.insert_one(new_user)
        user_id = str(result.inserted_id)
        role = new_user["role"]

    access_token = create_access_token(
        data={"user_id": user_id, "email": user_email, "role": role},
        expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    
    response = RedirectResponse(url="/")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.post("/register")
async def register_user(user: UserRegister):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists."
        )

    hashed_password = get_password_hash(user.password)
    new_user = {
        "username" : user.username,
        "email": user.email,
        "name" : user.first_name + " " + user.last_name,
        "hashed_password": hashed_password,
        "role": "patient"
    }
    
    result = await users_collection.insert_one(new_user)    

    access_token = create_access_token(
        data={"user_id": str(result.inserted_id), "email": user.email, "role": "patient"},
        expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login_user(user : UserLogin):
    user_in_db = await users_collection.find_one({
        "$or": [
            {"email": user.username_or_email},
            {"username": user.username_or_email}
        ]
    })

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not verify_password(user.password, user_in_db["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        data={"user_id": str(user_in_db["_id"]), "email": user_in_db["email"], "role": user_in_db["role"]},
        expires_delta=timedelta(minutes=15)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return user

@router.post("/onboard/doctor")
async def onboard_doctor(user=Depends(get_current_user)):
    if user.get("role") == "doctor" or user.get("role") == "pending_doctor":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role change already initiated.")


    await users_collection.update_one(
        {"_id": ObjectId(user["user_id"])},
        {"$set": {"role": "pending_doctor"}}
    )
    
    return {"message": "Verification requested. Please provide license details."}


@router.post("/verify/doctor")
async def verify_doctor(
    verification_details: VerificationDetails,
    user=Depends(get_current_user)
):
    if user.get("role") != "pending_doctor":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role verification not requested.")    
    
    await initialize_doctor_licenses()

    is_license_valid = await doctor_licenses_collection.find_one(
        {"license_number": verification_details.license_number, "email": user.get("email")}
    )
    
    if not is_license_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid license number or email.")    

    await users_collection.update_one(
        {"_id": ObjectId(user["user_id"])},
        {"$set": {"role": "doctor"}}
    )
    new_payload = {
        "user_id" : user["user_id"],
        "email": user["email"],
        "role": "doctor"
    }
    new_access_token = create_access_token(new_payload, expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    
    return {
        "message": "Verification successful. Your role has been updated.",
        "access_token":new_access_token,
        "token_type": "bearer"
        }