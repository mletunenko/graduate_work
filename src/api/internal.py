from fastapi import APIRouter

from db.postgres import SessionDep
from schemas.profile import UpdateEmailRequest
from services.profile import ProfileService

router = APIRouter(prefix="/internal", tags=["internal"])


@router.post("/update-email")
async def update_email(
    data: UpdateEmailRequest,
    session: SessionDep,
):
    await ProfileService.update_email(data, session)
    return {"status": "OK"}
