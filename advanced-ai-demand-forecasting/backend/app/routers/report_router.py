import os
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.report import Report
from app.schemas.report_schema import ReportCreateRequest
from app.utils.auth import get_current_user
from app.utils.pagination import paginate
from app.services.report_service import generate_report, format_report

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)


@router.post("/generate")
def create_report(
    request: ReportCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = generate_report(
        db=db,
        forecast_id=request.forecast_id,
        report_type=request.report_type,
        user_id=current_user.id,
        role=current_user.role
    )

    return {
        "success": True,
        "message": "Report generated successfully",
        "data": format_report(report)
    }


@router.get("/")
def list_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    report_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Report)

    if current_user.role != "admin":
        query = query.filter(Report.user_id == current_user.id)

    if report_type:
        query = query.filter(Report.report_type == report_type)

    query = query.order_by(Report.created_at.desc())

    result = paginate(query, page, limit)

    return {
        "success": True,
        "message": "Reports fetched successfully",
        "data": {
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "total_pages": result["total_pages"],
            "items": [format_report(item) for item in result["items"]]
        }
    }


@router.get("/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    if current_user.role != "admin" and report.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this report"
        )

    return {
        "success": True,
        "message": "Report fetched successfully",
        "data": format_report(report)
    }


@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    if current_user.role != "admin" and report.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to download this report"
        )

    if not report.file_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This report does not have a downloadable file"
        )

    if not os.path.exists(report.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found"
        )

    filename = os.path.basename(report.file_path)

    return FileResponse(
        path=report.file_path,
        filename=filename,
        media_type="application/octet-stream"
    )


@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    if current_user.role != "admin" and report.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this report"
        )

    if report.file_path and os.path.exists(report.file_path):
        os.remove(report.file_path)

    db.delete(report)
    db.commit()

    return {
        "success": True,
        "message": "Report deleted successfully"
    }