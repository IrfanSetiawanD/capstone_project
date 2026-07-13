"""
Latih dan bandingkan 2 model buat prediksi revenue harian:
- Linear Regression  → baseline sederhana
- Random Forest      → nangkep pola non-linear (efek weekend, gajian, dll)

Karena data historis masih pendek (hitungan minggu), evaluasi TIDAK pakai
random train-test split — itu bakal bocor informasi masa depan ke masa
lalu. Yang benar buat time series: split berurutan (train = hari-hari
awal, test = hari-hari terakhir).
"""
import json
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
from django.conf import settings
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

from .data import FEATURE_COLUMNS, MIN_DAYS_REQUIRED, get_training_data

MODEL_DIR = Path(__file__).resolve().parent.parent / 'saved_models'
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / 'revenue_model.joblib'
METADATA_PATH = MODEL_DIR / 'metadata.json'

TEST_SIZE_DAYS = 7  # sisihkan 7 hari terakhir buat evaluasi out-of-sample


def _evaluate(y_true, y_pred):
    return {
        'mae': float(mean_absolute_error(y_true, y_pred)),
        'rmse': float(np.sqrt(mean_squared_error(y_true, y_pred))),
        # MAPE dihitung manual dengan pengaman div-by-zero (hari revenue=0 bikin
        # mean_absolute_percentage_error bawaan sklearn meledak ke inf)
        'mape': float(
            np.mean([
                abs(t - p) / t if t != 0 else 0.0
                for t, p in zip(y_true, y_pred)
            ]) * 100
        ),
    }


def train_and_select_best():
    """
    Latih kedua model, evaluasi di 7 hari terakhir, pilih yang MAE-nya
    lebih kecil, lalu retrain model terpilih pakai SEMUA data (biar model
    final yang disimpan memanfaatkan histori penuh, bukan cuma data train).

    Return dict berisi status & metrik — dilempar apa adanya ke caller
    (management command / view) buat ditampilkan.
    """
    X, y, _ = get_training_data()

    if X is None or len(X) < MIN_DAYS_REQUIRED:
        return {
            'success': False,
            'reason': f'Data historis kurang dari {MIN_DAYS_REQUIRED} hari '
                      f'(ada {0 if X is None else len(X)} hari). Butuh lebih banyak transaksi completed.',
        }

    if len(X) <= TEST_SIZE_DAYS + 5:
        # Data terlalu pendek buat disisihkan test set yang berarti —
        # tetap latih, tapi skip evaluasi out-of-sample yang proper.
        split_idx = max(1, len(X) - 3)
    else:
        split_idx = len(X) - TEST_SIZE_DAYS

    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    candidates = {
        'linear_regression': LinearRegression(),
        'random_forest': RandomForestRegressor(
            n_estimators=200,
            max_depth=5,          # dibatasi — data dikit, gampang overfit kalau dalem
            min_samples_leaf=2,
            random_state=42,
        ),
    }

    results = {}
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        preds = np.clip(preds, a_min=0, a_max=None)  # revenue gak mungkin negatif
        results[name] = _evaluate(y_test.values, preds)

    best_name = min(results, key=lambda k: results[k]['mae'])
    best_model = candidates[best_name]

    # Retrain model terpilih pakai seluruh data (train+test) buat produksi
    best_model.fit(X, y)

    joblib.dump(best_model, MODEL_PATH)

    metadata = {
        'trained_at': datetime.now().isoformat(),
        'best_model': best_name,
        'n_training_days': int(len(X)),
        'feature_columns': FEATURE_COLUMNS,
        'metrics': results,
    }
    with open(METADATA_PATH, 'w') as f:
        json.dump(metadata, f, indent=2)

    return {'success': True, **metadata}
