"""
Generate prediksi revenue N hari ke depan.

Karena fitur model termasuk lag_1 (revenue kemarin) dan rolling_avg_7,
prediksi harus dilakukan RECURSIVE: prediksi besok dulu, baru hasilnya
dipakai sebagai "lag_1" buat prediksi lusa, dst. Ini pendekatan standar
buat regression model yang dipakai forecasting time series (bukan model
time-series murni kayak ARIMA yang punya mekanisme sendiri).
"""
import json
from datetime import timedelta

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

from .data import FEATURE_COLUMNS, get_daily_revenue_df, add_features
from .train import MODEL_PATH, METADATA_PATH


class ModelNotTrainedError(Exception):
    pass


def _build_features_for_date(date, history: pd.Series):
    """
    history: pandas Series revenue harian yang sudah terisi sampai
    tanggal sebelum `date` (index = tanggal).
    """
    day_of_week = date.dayofweek
    is_weekend = int(day_of_week >= 5)
    day_of_month = date.day
    is_payday_period = int(day_of_month >= 25 or day_of_month <= 5)

    lag_1 = history.iloc[-1] if len(history) >= 1 else 0.0
    lag_7 = history.iloc[-7] if len(history) >= 7 else history.mean() if len(history) else 0.0
    rolling_avg_7 = history.iloc[-7:].mean() if len(history) >= 1 else 0.0

    return {
        'day_of_week': day_of_week,
        'is_weekend': is_weekend,
        'day_of_month': day_of_month,
        'is_payday_period': is_payday_period,
        'lag_1': lag_1,
        'lag_7': lag_7,
        'rolling_avg_7': rolling_avg_7,
    }


def _predict_with_interval(model, X_pred):
    """
    Random Forest: tiap pohon di dalam forest punya "pendapat" sendiri-sendiri.
    Sebaran pendapat itu dipakai sebagai proxy confidence interval (persentil
    10-90 dari prediksi semua pohon) — pendekatan umum buat RF karena dia gak
    punya rumus interval bawaan kayak regresi linear.

    Linear Regression: gak punya noise per-estimator kayak RF, jadi interval
    dibikin lebar tetap ±15% dari titik prediksi sebagai perkiraan kasar
    (ditandain di response sebagai interval kasar, bukan statistik ketat).
    """
    point = float(model.predict(X_pred)[0])
    point = max(point, 0.0)

    if isinstance(model, RandomForestRegressor):
        X_arr = X_pred.values
        tree_preds = np.array([tree.predict(X_arr)[0] for tree in model.estimators_])
        tree_preds = np.clip(tree_preds, a_min=0, a_max=None)
        lower = float(np.percentile(tree_preds, 10))
        upper = float(np.percentile(tree_preds, 90))
    else:
        lower = point * 0.85
        upper = point * 1.15

    lower = max(min(lower, point), 0.0)
    upper = max(upper, point)
    return point, lower, upper


def forecast(n_days: int = 30, history_days: int = 30):
    """
    Return dict siap pakai buat dashboard: data historis (buat garis solid
    di chart), prediksi n_days ke depan (buat garis putus-putus + band
    confidence interval), dan total 7-hari-ke-depan buat stat card.
    """
    if not MODEL_PATH.exists():
        raise ModelNotTrainedError('Model belum pernah dilatih. Jalankan training dulu.')

    model = joblib.load(MODEL_PATH)
    with open(METADATA_PATH) as f:
        metadata = json.load(f)

    daily = get_daily_revenue_df()
    if daily.empty:
        raise ModelNotTrainedError('Tidak ada data historis buat dasar prediksi.')

    history = daily.set_index('date')['revenue']
    last_date = history.index.max()

    predictions = []
    working_history = history.copy()

    for i in range(1, n_days + 1):
        target_date = last_date + timedelta(days=i)
        feats = _build_features_for_date(target_date, working_history)
        X_pred = pd.DataFrame([feats])[FEATURE_COLUMNS]
        point, lower, upper = _predict_with_interval(model, X_pred)

        predictions.append({
            'date': target_date.strftime('%Y-%m-%d'),
            'predicted_revenue': round(point, 0),
            'lower': round(lower, 0),
            'upper': round(upper, 0),
        })

        # Masukin hasil prediksi ke history biar bisa jadi lag buat hari berikutnya
        working_history.loc[target_date] = point

    total = sum(p['predicted_revenue'] for p in predictions)
    next_7_days_total = sum(p['predicted_revenue'] for p in predictions[:7])

    history_tail = daily.tail(history_days)
    history_out = [
        {'date': row.date.strftime('%Y-%m-%d'), 'revenue': round(float(row.revenue), 0)}
        for row in history_tail.itertuples()
    ]

    return {
        'history': history_out,
        'predictions': predictions,
        'total_predicted_revenue': round(total, 0),
        'next_7_days_total': round(next_7_days_total, 0),
        'model_used': metadata.get('best_model'),
        'trained_at': metadata.get('trained_at'),
        'model_metrics': metadata.get('metrics'),
        'last_actual_date': last_date.strftime('%Y-%m-%d'),
        'n_training_days': metadata.get('n_training_days'),
    }
