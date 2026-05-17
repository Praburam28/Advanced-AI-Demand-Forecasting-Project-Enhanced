import os
import json
import pandas as pd

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.models.forecast import ForecastHistory
from app.services.notification_service import create_notification
from app.ml.models import (
    prepare_series,
    run_forecast_model,
    build_prediction_output,
    compare_all_models,
    SUPPORTED_MODELS
)


def read_dataset_file(dataset: Dataset):
    if not os.path.exists(dataset.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset file not found"
        )

    try:
        if dataset.file_type == "csv":
            return pd.read_csv(dataset.file_path)

        return pd.read_excel(dataset.file_path)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to read dataset: {str(e)}"
        )


def generate_forecast(
    db: Session,
    dataset_id: int,
    user_id: int,
    target_column: str,
    date_column: str | None,
    model_name: str,
    forecast_periods: int
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    if forecast_periods < 1 or forecast_periods > 365:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Forecast periods must be between 1 and 365"
        )

    if model_name not in SUPPORTED_MODELS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported model. Supported models: {SUPPORTED_MODELS}"
        )

    df = read_dataset_file(dataset)

    try:
        prepared_df, series = prepare_series(
            df=df,
            target_column=target_column,
            date_column=date_column
        )

        metrics, future_predictions = run_forecast_model(
            model_name=model_name,
            series=series,
            forecast_periods=forecast_periods
        )

        predictions = build_prediction_output(
            future_predictions=future_predictions,
            forecast_periods=forecast_periods
        )

    except Exception as e:
        create_notification(
            db=db,
            user_id=user_id,
            title="Forecast Generation Failed",
            message=str(e),
            type="error"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    forecast = ForecastHistory(
        dataset_id=dataset_id,
        user_id=user_id,
        model_name=model_name,
        target_column=target_column,
        date_column=date_column,
        forecast_periods=forecast_periods,
        mae=metrics["mae"],
        rmse=metrics["rmse"],
        mape=metrics["mape"],
        predictions=json.dumps(predictions)
    )

    db.add(forecast)
    db.commit()
    db.refresh(forecast)

    create_notification(
        db=db,
        user_id=user_id,
        title="Forecast Generated",
        message=f"{model_name} forecast completed for dataset '{dataset.name}'.",
        type="success"
    )

    return forecast


def generate_model_comparison(
    db: Session,
    dataset_id: int,
    user_id: int,
    target_column: str,
    date_column: str | None,
    forecast_periods: int
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    df = read_dataset_file(dataset)

    try:
        prepared_df, series = prepare_series(
            df=df,
            target_column=target_column,
            date_column=date_column
        )

        comparison_result = compare_all_models(
            series=series,
            forecast_periods=forecast_periods
        )

    except Exception as e:
        create_notification(
            db=db,
            user_id=user_id,
            title="Model Comparison Failed",
            message=str(e),
            type="error"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    best_model = comparison_result.get("best_model")

    forecast = ForecastHistory(
        dataset_id=dataset_id,
        user_id=user_id,
        model_name=best_model["model_name"] if best_model else "comparison",
        target_column=target_column,
        date_column=date_column,
        forecast_periods=forecast_periods,
        mae=best_model.get("mae") if best_model else None,
        rmse=best_model.get("rmse") if best_model else None,
        mape=best_model.get("mape") if best_model else None,
        predictions=json.dumps(best_model.get("predictions") if best_model else []),
        comparison_result=json.dumps(comparison_result)
    )

    db.add(forecast)
    db.commit()
    db.refresh(forecast)

    create_notification(
        db=db,
        user_id=user_id,
        title="Model Comparison Completed",
        message=f"Best model: {best_model['model_name'] if best_model else 'Not available'}",
        type="success"
    )

    return forecast


def format_forecast_history(forecast: ForecastHistory):
    predictions = []
    comparison_result = None

    if forecast.predictions:
        try:
            predictions = json.loads(forecast.predictions)
        except Exception:
            predictions = forecast.predictions

    if forecast.comparison_result:
        try:
            comparison_result = json.loads(forecast.comparison_result)
        except Exception:
            comparison_result = forecast.comparison_result

    return {
        "id": forecast.id,
        "dataset_id": forecast.dataset_id,
        "user_id": forecast.user_id,
        "model_name": forecast.model_name,
        "target_column": forecast.target_column,
        "date_column": forecast.date_column,
        "forecast_periods": forecast.forecast_periods,
        "mae": forecast.mae,
        "rmse": forecast.rmse,
        "mape": forecast.mape,
        "predictions": predictions,
        "comparison_result": comparison_result,
        "created_at": forecast.created_at
    }