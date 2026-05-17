import json
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast import ForecastHistory
from app.schemas.user_schema import UserUpdate
from app.utils.auth import require_admin
from app.utils.pagination import paginate
from app.services.admin_service import (
    get_admin_overview,
    user_growth_chart,
    dataset_upload_chart,
    forecast_activity_chart_admin,
    model_usage_admin,
    top_active_users
)
from app.services.forecast_service import format_forecast_history

from app.models.report import Report
from app.services.report_service import format_report



router = APIRouter(
    prefix="/api/admin",
    tags=["Admin Panel"]
)


def format_user(user: User):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at
    }


def format_dataset_admin(dataset: Dataset):
    columns_info = None

    if dataset.columns_info:
        try:
            columns_info = json.loads(dataset.columns_info)
        except Exception:
            columns_info = dataset.columns_info

    return {
        "id": dataset.id,
        "name": dataset.name,
        "file_name": dataset.file_name,
        "file_type": dataset.file_type,
        "total_rows": dataset.total_rows,
        "total_columns": dataset.total_columns,
        "columns_info": columns_info,
        "product_category": dataset.product_category,
        "region": dataset.region,
        "uploaded_by": dataset.uploaded_by,
        "created_at": dataset.created_at
    }


@router.get("/overview")
def admin_overview(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return {
        "success": True,
        "message": "Admin overview fetched successfully",
        "data": get_admin_overview(db)
    }


@router.get("/analytics")
def admin_analytics(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return {
        "success": True,
        "message": "Admin analytics fetched successfully",
        "data": {
            "user_growth": user_growth_chart(db),
            "dataset_uploads": dataset_upload_chart(db),
            "forecast_activity": forecast_activity_chart_admin(db),
            "model_usage": model_usage_admin(db),
            "top_active_users": top_active_users(db)
        }
    }


@router.get("/users")
def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    query = db.query(User)

    if search:
        query = query.filter(
            (User.name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    query = query.order_by(User.created_at.desc())

    result = paginate(query, page, limit)

    return {
        "success": True,
        "message": "Users fetched successfully",
        "data": {
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "total_pages": result["total_pages"],
            "items": [format_user(item) for item in result["items"]]
        }
    }


@router.get("/users/{user_id}")
def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "success": True,
        "message": "User detail fetched successfully",
        "data": format_user(user)
    }


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if payload.name is not None:
        user.name = payload.name

    if payload.role is not None:
        if payload.role not in ["user", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role must be either user or admin"
            )
        user.role = payload.role

    if payload.is_active is not None:
        user.is_active = payload.is_active

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "User updated successfully",
        "data": format_user(user)
    }


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin cannot delete own account"
        )

    db.delete(user)
    db.commit()

    return {
        "success": True,
        "message": "User deleted successfully"
    }


@router.get("/datasets")
def admin_datasets(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    product_category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    query = db.query(Dataset)

    if search:
        query = query.filter(Dataset.name.ilike(f"%{search}%"))

    if product_category:
        query = query.filter(Dataset.product_category == product_category)

    if region:
        query = query.filter(Dataset.region == region)

    query = query.order_by(Dataset.created_at.desc())

    result = paginate(query, page, limit)

    return {
        "success": True,
        "message": "All datasets fetched successfully",
        "data": {
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "total_pages": result["total_pages"],
            "items": [format_dataset_admin(item) for item in result["items"]]
        }
    }


@router.get("/forecasts")
def admin_forecasts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    model_name: Optional[str] = Query(None),
    dataset_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    query = db.query(ForecastHistory)

    if model_name:
        query = query.filter(ForecastHistory.model_name == model_name)

    if dataset_id:
        query = query.filter(ForecastHistory.dataset_id == dataset_id)

    if user_id:
        query = query.filter(ForecastHistory.user_id == user_id)

    query = query.order_by(ForecastHistory.created_at.desc())

    result = paginate(query, page, limit)

    return {
        "success": True,
        "message": "All forecasts fetched successfully",
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
    
@router.get("/reports")
def admin_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    report_type: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    query = db.query(Report)

    if report_type:
        query = query.filter(Report.report_type == report_type)

    if user_id:
        query = query.filter(Report.user_id == user_id)

    query = query.order_by(Report.created_at.desc())

    result = paginate(query, page, limit)

    return {
        "success": True,
        "message": "All reports fetched successfully",
        "data": {
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "total_pages": result["total_pages"],
            "items": [
                format_report(item)
                for item in result["items"]
            ]
        }
    }