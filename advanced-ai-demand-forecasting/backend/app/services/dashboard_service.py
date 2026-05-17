from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.dataset import Dataset
from app.models.forecast import ForecastHistory
from app.models.user import User


def dashboard_summary(db: Session, current_user: User):
    dataset_query = db.query(Dataset)
    forecast_query = db.query(ForecastHistory)

    if current_user.role != "admin":
        dataset_query = dataset_query.filter(Dataset.uploaded_by == current_user.id)
        forecast_query = forecast_query.filter(ForecastHistory.user_id == current_user.id)

    total_datasets = dataset_query.count()
    total_forecasts = forecast_query.count()

    avg_mae = forecast_query.with_entities(func.avg(ForecastHistory.mae)).scalar()
    avg_rmse = forecast_query.with_entities(func.avg(ForecastHistory.rmse)).scalar()
    avg_mape = forecast_query.with_entities(func.avg(ForecastHistory.mape)).scalar()

    return {
        "total_datasets": total_datasets,
        "total_forecasts": total_forecasts,
        "average_mae": round(float(avg_mae), 4) if avg_mae else 0,
        "average_rmse": round(float(avg_rmse), 4) if avg_rmse else 0,
        "average_mape": round(float(avg_mape), 4) if avg_mape else 0
    }


def apply_dashboard_filters(query, start_date=None, end_date=None):
    if start_date:
        query = query.filter(ForecastHistory.created_at >= start_date)

    if end_date:
        query = query.filter(ForecastHistory.created_at <= end_date)

    return query


def forecast_activity_chart(
    db: Session,
    current_user: User,
    start_date: datetime | None = None,
    end_date: datetime | None = None
):
    query = db.query(
        func.date(ForecastHistory.created_at).label("date"),
        func.count(ForecastHistory.id).label("count")
    )

    if current_user.role != "admin":
        query = query.filter(ForecastHistory.user_id == current_user.id)

    query = apply_dashboard_filters(query, start_date, end_date)

    data = (
        query.group_by(func.date(ForecastHistory.created_at))
        .order_by(func.date(ForecastHistory.created_at))
        .all()
    )

    return [
        {
            "date": str(row.date),
            "forecast_count": row.count
        }
        for row in data
    ]


def model_usage_chart(
    db: Session,
    current_user: User,
    start_date: datetime | None = None,
    end_date: datetime | None = None
):
    query = db.query(
        ForecastHistory.model_name,
        func.count(ForecastHistory.id).label("count")
    )

    if current_user.role != "admin":
        query = query.filter(ForecastHistory.user_id == current_user.id)

    query = apply_dashboard_filters(query, start_date, end_date)

    data = (
        query.group_by(ForecastHistory.model_name)
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


def model_performance_chart(
    db: Session,
    current_user: User,
    start_date: datetime | None = None,
    end_date: datetime | None = None
):
    query = db.query(
        ForecastHistory.model_name,
        func.avg(ForecastHistory.mae).label("avg_mae"),
        func.avg(ForecastHistory.rmse).label("avg_rmse"),
        func.avg(ForecastHistory.mape).label("avg_mape")
    )

    if current_user.role != "admin":
        query = query.filter(ForecastHistory.user_id == current_user.id)

    query = apply_dashboard_filters(query, start_date, end_date)

    data = query.group_by(ForecastHistory.model_name).all()

    return [
        {
            "model_name": row.model_name,
            "average_mae": round(float(row.avg_mae), 4) if row.avg_mae else 0,
            "average_rmse": round(float(row.avg_rmse), 4) if row.avg_rmse else 0,
            "average_mape": round(float(row.avg_mape), 4) if row.avg_mape else 0
        }
        for row in data
    ]


def dataset_category_chart(db: Session, current_user: User):
    query = db.query(
        Dataset.product_category,
        func.count(Dataset.id).label("count")
    )

    if current_user.role != "admin":
        query = query.filter(Dataset.uploaded_by == current_user.id)

    data = (
        query.group_by(Dataset.product_category)
        .order_by(func.count(Dataset.id).desc())
        .all()
    )

    return [
        {
            "product_category": row.product_category or "Uncategorized",
            "count": row.count
        }
        for row in data
    ]


def dataset_region_chart(db: Session, current_user: User):
    query = db.query(
        Dataset.region,
        func.count(Dataset.id).label("count")
    )

    if current_user.role != "admin":
        query = query.filter(Dataset.uploaded_by == current_user.id)

    data = (
        query.group_by(Dataset.region)
        .order_by(func.count(Dataset.id).desc())
        .all()
    )

    return [
        {
            "region": row.region or "Unknown",
            "count": row.count
        }
        for row in data
    ]


def recent_forecast_activity(db: Session, current_user: User, limit: int = 10):
    query = db.query(ForecastHistory)

    if current_user.role != "admin":
        query = query.filter(ForecastHistory.user_id == current_user.id)

    records = (
        query.order_by(ForecastHistory.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": item.id,
            "dataset_id": item.dataset_id,
            "model_name": item.model_name,
            "target_column": item.target_column,
            "forecast_periods": item.forecast_periods,
            "mae": item.mae,
            "rmse": item.rmse,
            "mape": item.mape,
            "created_at": item.created_at
        }
        for item in records
    ]


def dashboard_filters(db: Session, current_user: User):
    dataset_query = db.query(Dataset)

    if current_user.role != "admin":
        dataset_query = dataset_query.filter(Dataset.uploaded_by == current_user.id)

    categories = (
        dataset_query.with_entities(Dataset.product_category)
        .distinct()
        .all()
    )

    regions = (
        dataset_query.with_entities(Dataset.region)
        .distinct()
        .all()
    )

    return {
        "product_categories": [
            item.product_category for item in categories if item.product_category
        ],
        "regions": [
            item.region for item in regions if item.region
        ]
    }