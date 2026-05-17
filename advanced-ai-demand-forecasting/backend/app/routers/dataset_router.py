import json
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.dataset import Dataset
from app.schemas.dataset_schema import DatasetResponse
from app.services.dataset_service import (
    save_dataset_file,
    get_dataset_by_id,
    delete_dataset_by_id
)
from app.utils.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter(
    prefix="/api/datasets",
    tags=["Datasets"]
)


def format_dataset(dataset: Dataset):
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


@router.post("/upload")
def upload_dataset(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None),
    product_category: Optional[str] = Form(None),
    region: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dataset = save_dataset_file(
        db=db,
        file=file,
        user_id=current_user.id,
        name=name,
        product_category=product_category,
        region=region
    )

    return {
        "success": True,
        "message": "Dataset uploaded successfully",
        "data": format_dataset(dataset)
    }


@router.get("/")
def list_datasets(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    product_category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Dataset)

    if current_user.role != "admin":
        query = query.filter(Dataset.uploaded_by == current_user.id)

    if search:
        query = query.filter(Dataset.name.ilike(f"%{search}%"))

    if product_category:
        query = query.filter(Dataset.product_category == product_category)

    if region:
        query = query.filter(Dataset.region == region)

    if start_date:
        query = query.filter(Dataset.created_at >= start_date)

    if end_date:
        query = query.filter(Dataset.created_at <= end_date)

    query = query.order_by(Dataset.created_at.desc())

    result = paginate(query, page, limit)

    return {
        "success": True,
        "message": "Datasets fetched successfully",
        "data": {
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "total_pages": result["total_pages"],
            "items": [format_dataset(item) for item in result["items"]]
        }
    }


@router.get("/{dataset_id}")
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dataset = get_dataset_by_id(db, dataset_id)

    if current_user.role != "admin" and dataset.uploaded_by != current_user.id:
        return {
            "success": False,
            "message": "You do not have permission to access this dataset"
        }

    return {
        "success": True,
        "message": "Dataset fetched successfully",
        "data": format_dataset(dataset)
    }


@router.delete("/{dataset_id}")
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dataset = get_dataset_by_id(db, dataset_id)

    if current_user.role != "admin" and dataset.uploaded_by != current_user.id:
        return {
            "success": False,
            "message": "You do not have permission to delete this dataset"
        }

    delete_dataset_by_id(db, dataset_id)

    return {
        "success": True,
        "message": "Dataset deleted successfully"
    }