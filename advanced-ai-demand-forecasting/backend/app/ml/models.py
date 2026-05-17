import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.arima.model import ARIMA

from app.ml.evaluator import calculate_metrics


SUPPORTED_MODELS = [
    "linear_regression",
    "random_forest",
    "arima",
    "moving_average"
]


def prepare_series(df: pd.DataFrame, target_column: str, date_column: str | None = None):
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found")

    data = df.copy()

    if date_column:
        if date_column not in data.columns:
            raise ValueError(f"Date column '{date_column}' not found")

        data[date_column] = pd.to_datetime(data[date_column], errors="coerce")
        data = data.dropna(subset=[date_column])
        data = data.sort_values(date_column)

    data[target_column] = pd.to_numeric(data[target_column], errors="coerce")
    data = data.dropna(subset=[target_column])

    if len(data) < 10:
        raise ValueError("Dataset must contain at least 10 valid rows for forecasting")

    series = data[target_column].values

    return data, series


def train_test_split_series(series):
    split_index = int(len(series) * 0.8)

    train = series[:split_index]
    test = series[split_index:]

    if len(test) == 0:
        test = series[-2:]
        train = series[:-2]

    return train, test


def linear_regression_forecast(series, forecast_periods):
    train, test = train_test_split_series(series)

    x_train = np.arange(len(train)).reshape(-1, 1)
    y_train = train

    x_test = np.arange(len(train), len(train) + len(test)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(x_train, y_train)

    test_predictions = model.predict(x_test)

    future_x = np.arange(len(series), len(series) + forecast_periods).reshape(-1, 1)
    future_predictions = model.predict(future_x)

    metrics = calculate_metrics(test, test_predictions)

    return metrics, future_predictions


def random_forest_forecast(series, forecast_periods):
    train, test = train_test_split_series(series)

    x_train = np.arange(len(train)).reshape(-1, 1)
    y_train = train

    x_test = np.arange(len(train), len(train) + len(test)).reshape(-1, 1)

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(x_train, y_train)

    test_predictions = model.predict(x_test)

    future_x = np.arange(len(series), len(series) + forecast_periods).reshape(-1, 1)
    future_predictions = model.predict(future_x)

    metrics = calculate_metrics(test, test_predictions)

    return metrics, future_predictions


def moving_average_forecast(series, forecast_periods):
    train, test = train_test_split_series(series)

    window = min(5, len(train))
    moving_avg_value = np.mean(train[-window:])

    test_predictions = np.array([moving_avg_value] * len(test))
    future_predictions = np.array([moving_avg_value] * forecast_periods)

    metrics = calculate_metrics(test, test_predictions)

    return metrics, future_predictions


def arima_forecast(series, forecast_periods):
    train, test = train_test_split_series(series)

    try:
        model = ARIMA(train, order=(2, 1, 2))
        model_fit = model.fit()

        test_predictions = model_fit.forecast(steps=len(test))
        future_predictions = model_fit.forecast(steps=forecast_periods)

        metrics = calculate_metrics(test, test_predictions)

        return metrics, future_predictions

    except Exception:
        return moving_average_forecast(series, forecast_periods)


def run_forecast_model(model_name, series, forecast_periods):
    if model_name == "linear_regression":
        return linear_regression_forecast(series, forecast_periods)

    if model_name == "random_forest":
        return random_forest_forecast(series, forecast_periods)

    if model_name == "arima":
        return arima_forecast(series, forecast_periods)

    if model_name == "moving_average":
        return moving_average_forecast(series, forecast_periods)

    raise ValueError(f"Unsupported model: {model_name}")


def build_prediction_output(future_predictions, forecast_periods):
    predictions = []

    for i in range(forecast_periods):
        predictions.append({
            "period": i + 1,
            "predicted_value": round(float(future_predictions[i]), 2)
        })

    return predictions


def compare_all_models(series, forecast_periods):
    results = []

    for model_name in SUPPORTED_MODELS:
        try:
            metrics, future_predictions = run_forecast_model(
                model_name=model_name,
                series=series,
                forecast_periods=forecast_periods
            )

            results.append({
                "model_name": model_name,
                "mae": metrics["mae"],
                "rmse": metrics["rmse"],
                "mape": metrics["mape"],
                "predictions": build_prediction_output(
                    future_predictions,
                    forecast_periods
                )
            })

        except Exception as e:
            results.append({
                "model_name": model_name,
                "error": str(e)
            })

    valid_results = [item for item in results if "rmse" in item]

    best_model = None

    if valid_results:
        best_model = min(valid_results, key=lambda x: x["rmse"])

    return {
        "best_model": best_model,
        "models": results
    }