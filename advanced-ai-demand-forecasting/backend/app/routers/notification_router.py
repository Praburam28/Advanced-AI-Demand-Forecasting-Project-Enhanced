from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.notification import Notification
from app.utils.auth import get_current_user
from app.utils.pagination import paginate
from app.services.notification_service import (
    get_user_notifications,
    get_unread_count,
    mark_notification_as_read,
    mark_all_notifications_as_read,
    delete_notification
)

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)


def format_notification(notification: Notification):
    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "title": notification.title,
        "message": notification.message,
        "type": notification.type,
        "is_read": notification.is_read,
        "created_at": notification.created_at
    }


@router.get("/")
def list_notifications(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    only_unread: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = get_user_notifications(
        db=db,
        user_id=current_user.id,
        only_unread=only_unread
    )

    result = paginate(query, page, limit)

    return {
        "success": True,
        "message": "Notifications fetched successfully",
        "data": {
            "page": result["page"],
            "limit": result["limit"],
            "total": result["total"],
            "total_pages": result["total_pages"],
            "items": [
                format_notification(item)
                for item in result["items"]
            ]
        }
    }


@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "success": True,
        "message": "Unread notification count fetched successfully",
        "data": {
            "count": get_unread_count(db, current_user.id)
        }
    }


@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = mark_notification_as_read(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )

    return {
        "success": True,
        "message": "Notification marked as read",
        "data": format_notification(notification)
    }


@router.put("/read-all")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mark_all_notifications_as_read(db, current_user.id)

    return {
        "success": True,
        "message": "All notifications marked as read"
    }


@router.delete("/{notification_id}")
def remove_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_notification(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )

    return {
        "success": True,
        "message": "Notification deleted successfully"
    }