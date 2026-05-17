from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.forecast import ForecastHistory
from app.schemas.forecast_schema import ForecastRequest, ModelComparisonRequest
from app.services.forecast_service import (
    generate_forecast,
    generate_model_comparison,
    format_forecast_history
)
from app.utils.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter(
    prefix="/api/forecasts",
    tags=["Forecasting"]
)


@router.post("/generate")
def create_forecast(
    request: ForecastRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    forecast = generate_forecast(
        db=db,
        dataset_id=request.dataset_id,
        user_id=current_user.id,
        target_column=request.target_column,
        date_column=request.date_column,
        model_name=request.model_name,
        forecast_periods=request.forecast_periods
    )

    return {
        "success": True,
        "message": "Forecast generated successfully",
        "data": format_forecast_history(forecast)
    }


@router.post("/compare")
def compare_models(
    request: ModelComparisonRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    forecast = generate_model_comparison(
        db=db,
        dataset_id=request.dataset_id,
        user_id=current_user.id,
        target_column=request.target_column,
        date_column=request.date_column,
        forecast_periods=request.forecast_periods
    )

    return {
        "success": True,
        "message": "Model comparison completed successfully",
        "data": format_forecast_history(forecast)
    }


@router.get("/history")
def get_forecast_history(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    dataset_id: Optional[int] = Query(None),
    model_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ForecastHistory)

    if current_user.role != "admin":
        query = query.filter(ForecastHistory.user_id == current_user.id)

    if dataset_id:
        query = query.filter(ForecastHistory.dataset_id == dataset_id)

    if model_name:
        query = query.filter(ForecastHistory.model_name == model_name)

    query = query.order_by(ForecastHistory.created_at.desc())

    result = paginate(query, page, limit)

    return {
        "success": True,
        "message": "Forecast history fetched successfully",
        "data": {
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "total_pages": result["total_pages"],
            "items": [
                format_forecast_history(item)
                for item in result["items"]
            ]
        }
    }


@router.get("/history/{forecast_id}")
def get_forecast_detail(
    forecast_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    forecast = db.query(ForecastHistory).filter(
        ForecastHistory.id == forecast_id
    ).first()

    if not forecast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forecast history not found"
        )

    if current_user.role != "admin" and forecast.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this forecast"
        )

    return {
        "success": True,
        "message": "Forecast detail fetched successfully",
        "data": format_forecast_history(forecast)
    }


@router.delete("/history/{forecast_id}")
def delete_forecast_history(
    forecast_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    forecast = db.query(ForecastHistory).filter(
        ForecastHistory.id == forecast_id
    ).first()

    if not forecast:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forecast history not found"
        )

    if current_user.role != "admin" and forecast.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this forecast"
        )

    db.delete(forecast)
    db.commit()

    return {
        "success": True,
        "message": "Forecast history deleted successfully"
    }


@router.get("/models")
def get_supported_models(
    current_user: User = Depends(get_current_user)
):
    return {
        "success": True,
        "message": "Supported models fetched successfully",
        "data": [
            {
                "name": "linear_regression",
                "display_name": "Linear Regression",
                "description": "Simple trend-based forecasting model"
            },
            {
                "name": "random_forest",
                "display_name": "Random Forest",
                "description": "Machine learning model for nonlinear demand patterns"
            },
            {
                "name": "arima",
                "display_name": "ARIMA",
                "description": "Time series model for sequential demand forecasting"
            },
            {
                "name": "moving_average",
                "display_name": "Moving Average",
                "description": "Baseline model using recent average demand"
            }
        ]
    }