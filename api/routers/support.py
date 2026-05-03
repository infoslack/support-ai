from fastapi import APIRouter, HTTPException
from models.support import SupportRequest, SupportResponse
from services.support import SupportService

router = APIRouter()
support_service = SupportService()


@router.post("/support", response_model=SupportResponse)
def support(request: SupportRequest):
    try:
        return support_service.handle(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
