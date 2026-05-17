from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class ReportCreateRequest(BaseModel):
    forecast_id: int
    report_type: str = "summary"


class ReportResponse(BaseModel):
    id: int
    user_id: int
    forecast_id: int
    dataset_id: int
    title: str
    report_type: str
    file_path: Optional[str]
    summary: Optional[Any]
    created_at: datetime

    class Config:
        from_attributes = True