from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast import ForecastHistory


def get_admin_overview(db: Session):
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    admin_users = db.query(User).filter(User.role == "admin").count()

    total_datasets = db.query(Dataset).count()
    total_forecasts = db.query(ForecastHistory).count()

    avg_mae = db.query(func.avg(ForecastHistory.mae)).scalar()
    avg_rmse = db.query(func.avg(ForecastHistory.rmse)).scalar()
    avg_mape = db.query(func.avg(ForecastHistory.mape)).scalar()

    return {
        "total_users": total_users,
        "active_users": active_users,
        "admin_users": admin_users,
        "total_datasets": total_datasets,
        "total_forecasts": total_forecasts,
        "average_mae": round(float(avg_mae), 4) if avg_mae else 0,
        "average_rmse": round(float(avg_rmse), 4) if avg_rmse else 0,
        "average_mape": round(float(avg_mape), 4) if avg_mape else 0
    }


def user_growth_chart(db: Session):
    data = (
        db.query(
            func.date(User.created_at).label("date"),
            func.count(User.id).label("count")
        )
        .group_by(func.date(User.created_at))
        .order_by(func.date(User.created_at))
        .all()
    )

    return [
        {
            "date": str(row.date),
            "users": row.count
        }
        for row in data
    ]


def dataset_upload_chart(db: Session):
    data = (
        db.query(
            func.date(Dataset.created_at).label("date"),
            func.count(Dataset.id).label("count")
        )
        .group_by(func.date(Dataset.created_at))
        .order_by(func.date(Dataset.created_at))
        .all()
    )

    return [
        {
            "date": str(row.date),
            "datasets": row.count
        }
        for row in data
    ]


def forecast_activity_chart_admin(db: Session):
    data = (
        db.query(
            func.date(ForecastHistory.created_at).label("date"),
            func.count(ForecastHistory.id).label("count")
        )
        .group_by(func.date(ForecastHistory.created_at))
        .order_by(func.date(ForecastHistory.created_at))
        .all()
    )

    return [
        {
            "date": str(row.date),
            "forecasts": row.count
        }
        for row in data
    ]


def model_usage_admin(db: Session):
    data = (
        db.query(
            ForecastHistory.model_name,
            func.count(ForecastHistory.id).label("count")
        )
        .group_by(ForecastHistory.model_name)
        .order_by(func.count(ForecastHistory.id).desc())
        .all()
    )

    return [
        {
            "model_name": row.model_name,
            "count": row.count
        }
        for row in data
    ]


def top_active_users(db: Session, limit: int = 10):
    data = (
        db.query(
            User.id,
            User.name,
            User.email,
            func.count(ForecastHistory.id).label("forecast_count")
        )
        .outerjoin(ForecastHistory, ForecastHistory.user_id == User.id)
        .group_by(User.id, User.name, User.email)
        .order_by(func.count(ForecastHistory.id).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": row.id,
            "name": row.name,
            "email": row.email,
            "forecast_count": row.forecast_count
        }
        for row in data
    ]