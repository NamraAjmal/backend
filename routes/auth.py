from pydantic import BaseModel
from fastapi import APIRouter, Depends
from supabase_client import supabase
from fastapi.responses import JSONResponse, Response
from routes.protected import get_current_user

router = APIRouter()


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
async def signup(data: AuthRequest):
    if not data.email or not data.password:
        return JSONResponse(status_code=400, content={"error": "Bad request"})
    response = supabase.auth.sign_up({"email": data.email, "password": data.password})
    return JSONResponse(
        status_code=201,
        content={"user": response.user.model_dump() if response.user else None},
    )


@router.post("/login")
async def login(data: AuthRequest):
    if not data.email or not data.password:
        return JSONResponse(status_code=400, content={"error": "Bad request"})
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": data.email, "password": data.password}
        )
        return JSONResponse(
            status_code=200,
            content={
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
            },
        )
    except Exception:
        return JSONResponse(
            status_code=401, content={"error": "Invalid login credentials"}
        )


@router.post("/logout")
async def logout(user=Depends(get_current_user)):
    supabase.auth.sign_out()
    return Response(status_code=204)
