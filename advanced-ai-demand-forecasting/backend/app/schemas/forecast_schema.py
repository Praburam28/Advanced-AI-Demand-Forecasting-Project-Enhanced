from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class ForecastRequest(BaseModel):
    dataset_id: int
    target_column: str
    date_column: Optional[str] = None
    model_name: str = "linear_regression"
    forecast_periods: int = 7


class ModelComparisonRequest(BaseModel):
    dataset_id: int
    target_column: str
    date_column: Optional[str] = None
    forecast_periods: int = 7


class ForecastHistoryResponse(BaseModel):
    id: int
    dataset_id: int
    user_id: int
    model_name: str
    target_column: str
    date_column: Optional[str]
    forecast_periods: int
    mae: Optional[float]
    rmse: Optional[float]
    mape: Optional[float]
    predictions: Any
    comparison_result: Optional[Any]
    created_at: datetime

    class Config:
        from_attributes = True