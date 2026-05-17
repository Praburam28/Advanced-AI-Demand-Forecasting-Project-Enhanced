import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def calculate_metrics(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)

    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))

    non_zero_actual = actual != 0

    if non_zero_actual.any():
        mape = np.mean(
            np.abs((actual[non_zero_actual] - predicted[non_zero_actual]) / actual[non_zero_actual])
        ) * 100
    else:
        mape = 0

    return {
        "mae": round(float(mae), 4),
        "rmse": round(float(rmse), 4),
        "mape": round(float(mape), 4)
    }