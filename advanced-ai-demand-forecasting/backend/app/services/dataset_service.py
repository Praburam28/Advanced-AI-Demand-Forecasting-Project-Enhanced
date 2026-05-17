import os
import json
import uuid
import pandas as pd

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.services.notification_service import create_notification


UPLOAD_DIR = "uploads"


def save_dataset_file(
    db: Session,
    file: UploadFile,
    user_id: int,
    name: str | None = None,
    product_category: str | None = None,
    region: str | None = None
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is required"
        )

    allowed_extensions = [".csv", ".xlsx", ".xls"]
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        create_notification(
            db=db,
            user_id=user_id,
            title="Dataset Upload Failed",
            message="Only CSV, XLSX, and XLS files are allowed.",
            type="error"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV, XLSX, and XLS files are allowed"
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    try:
        if file_ext == ".csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)

        create_notification(
            db=db,
            user_id=user_id,
            title="Dataset Upload Failed",
            message=f"Unable to read dataset file: {str(e)}",
            type="error"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to read dataset file: {str(e)}"
        )

    if df.empty:
        if os.path.exists(file_path):
            os.remove(file_path)

        create_notification(
            db=db,
            user_id=user_id,
            title="Dataset Upload Failed",
            message="Uploaded dataset is empty.",
            type="error"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded dataset is empty"
        )

    columns_info = {
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "sample_rows": df.head(5).fillna("").to_dict(orient="records")
    }

    dataset = Dataset(
        name=name or file.filename,
        file_name=file.filename,
        file_path=file_path,
        file_type=file_ext.replace(".", ""),
        total_rows=len(df),
        total_columns=len(df.columns),
        columns_info=json.dumps(columns_info),
        product_category=product_category,
        region=region,
        uploaded_by=user_id
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    create_notification(
        db=db,
        user_id=user_id,
        title="Dataset Uploaded Successfully",
        message=f"Dataset '{dataset.name}' uploaded successfully with {dataset.total_rows} rows.",
        type="success"
    )

    return dataset


def get_dataset_by_id(db: Session, dataset_id: int):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    return dataset


def delete_dataset_by_id(db: Session, dataset_id: int):
    dataset = get_dataset_by_id(db, dataset_id)

    if os.path.exists(dataset.file_path):
        os.remove(dataset.file_path)

    db.delete(dataset)
    db.commit()

    return True