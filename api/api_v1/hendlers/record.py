from fastapi import APIRouter
from schemas.record_schema import RecordAuth
from services.record_service import RecordService
from models.models_mongo import Records


record_router = APIRouter()


@record_router.post('/create_rec', summary="Create new record", response_model=Records)
async def create_record(data: RecordAuth):
    return await RecordService.create_record(data)