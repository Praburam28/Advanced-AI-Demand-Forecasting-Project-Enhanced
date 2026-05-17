from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from app.services.dashboard_service import (
    dashboard_summary,
    forecast_activity_chart,
    model_usage_chart,
    model_performance_chart,
    dataset_category_chart,
    dataset_region_chart,
    recent_forecast_activity,
    dashboard_filters
)

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "success": True,
        "message": "Dashboard summary fetched successfully",
        "data": dashboard_summary(db, current_user)
    }


@router.get("/analytics")
def get_dashboard_analytics(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "success": True,
        "message": "Dashboard analytics fetched successfully",
        "data": {
            "forecast_activity": forecast_activity_chart(
                db, current_user, start_date, end_date
            ),
            "model_usage": model_usage_chart(
                db, current_user, start_date, end_date
            ),
            "model_performance": model_performance_chart(
                db, current_user, start_date, end_date
            ),
            "dataset_categories": dataset_category_chart(db, current_user),
            "dataset_regions": dataset_region_chart(db, current_user)
        }
    }


@router.get("/recent-activity")
def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "success": True,
        "message": "Recent forecast activity fetched successfully",
        "data": recent_forecast_activity(db, current_user, limit)
    }


@router.get("/filters")
def get_dashboard_filters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "success": True,
        "message": "Dashboard filters fetched successfully",
        "data": dashboard_filters(db, current_user)
    }