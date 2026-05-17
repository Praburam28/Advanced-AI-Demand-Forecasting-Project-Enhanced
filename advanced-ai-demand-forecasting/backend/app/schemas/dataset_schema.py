from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class DatasetResponse(BaseModel):
    id: int
    name: str
    file_name: str
    file_type: str
    total_rows: int
    total_columns: int
    columns_info: Optional[Any] = None
    product_category: Optional[str] = None
    region: Optional[str] = None
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class DatasetListResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    items: list[DatasetResponse]