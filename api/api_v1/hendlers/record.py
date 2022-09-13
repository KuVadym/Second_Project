from fastapi import APIRouter, Depends
from schemas.record_schema import RecordAuth
from services.record_service import RecordService
from models.models_mongo import Records, User
from api.deps.user_deps import get_current_user


record_router = APIRouter()


@record_router.post('/create_rec', summary="Create new record", response_model=Records)
async def create_record(data: RecordAuth, current_user: User = Depends(get_current_user)):
    return await RecordService.create_record(current_user, data)