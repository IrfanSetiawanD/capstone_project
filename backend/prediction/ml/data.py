"""
Agregasi data Order (status=completed) jadi time series revenue harian,
lengkap dengan feature engineering buat training model prediksi.

Kenapa harian, bukan bulanan?
Data transaksi Masashimura baru jalan beberapa minggu. Kalau diagregasi
langsung ke level bulanan, cuma dapet 1-2 titik data — gak cukup buat
melatih model apapun. Diagregasi ke harian dulu (puluhan titik data),
baru hasil prediksi harian dijumlah jadi estimasi bulanan.
"""
from datetime import timedelta

import pandas as pd
from django.db.models import Sum
from django.utils import timezone

from order.models import Order


MIN_DAYS_REQUIRED = 14  # minimal riwayat harian biar model gak asal


def get_daily_revenue_df() -> pd.DataFrame:
    """
    Return DataFrame dengan kolom: date, revenue.
    Hanya order berstatus 'completed'. Hari tanpa transaksi diisi 0
    (bukan di-skip), supaya time series-nya kontinu — ini penting
    buat fitur lag & rolling average.
    """
    # Pakai values_list + pandas buat truncation tanggal (bukan TruncDate
    # dari Django) biar konversi timezone-nya konsisten dan gampang di-debug.
    rows = Order.objects.filter(status='completed').values_list('created_at', 'total_price')

    if not rows:
        return pd.DataFrame(columns=['date', 'revenue'])

    df = pd.DataFrame(list(rows), columns=['created_at', 'total_price'])
    df['created_at'] = pd.to_datetime(df['created_at'])
    # Konversi ke local time (Asia/Jakarta) biar pengelompokan "per hari"-nya
    # sesuai jam operasional warung, bukan UTC.
    if df['created_at'].dt.tz is not None:
        df['created_at'] = df['created_at'].dt.tz_convert('Asia/Jakarta')
    df['date'] = df['created_at'].dt.date
    df['total_price'] = df['total_price'].astype(float)

    daily = df.groupby('date', as_index=False)['total_price'].sum()
    daily.columns = ['date', 'revenue']
    daily['date'] = pd.to_datetime(daily['date'])

    # Isi hari yang bolong (warung tutup / gak ada order) dengan revenue 0
    full_range = pd.date_range(daily['date'].min(), daily['date'].max(), freq='D')
    daily = daily.set_index('date').reindex(full_range, fill_value=0.0)
    daily.index.name = 'date'
    daily = daily.reset_index().rename(columns={'index': 'date'})

    return daily


def add_features(daily: pd.DataFrame) -> pd.DataFrame:
    """
    Tambah kolom fitur ke DataFrame hasil get_daily_revenue_df().
    Fitur sengaja dibikin sederhana (bukan puluhan fitur) karena
    data historisnya masih pendek — makin banyak fitur, makin gampang
    overfit ke noise warung kecil.
    """
    df = daily.copy()
    df['day_of_week'] = df['date'].dt.dayofweek          # 0=Senin ... 6=Minggu
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['day_of_month'] = df['date'].dt.day
    # Periode gajian: tanggal 25 akhir bulan s/d tanggal 5 awal bulan
    df['is_payday_period'] = df['day_of_month'].apply(
        lambda d: 1 if (d >= 25 or d <= 5) else 0
    )

    # Lag features — revenue kemarin & revenue di hari-sama minggu lalu
    df['lag_1'] = df['revenue'].shift(1)
    df['lag_7'] = df['revenue'].shift(7)

    # Rolling average 7 hari terakhir (tidak termasuk hari itu sendiri)
    df['rolling_avg_7'] = df['revenue'].shift(1).rolling(window=7, min_periods=1).mean()

    return df


FEATURE_COLUMNS = [
    'day_of_week', 'is_weekend', 'day_of_month', 'is_payday_period',
    'lag_1', 'lag_7', 'rolling_avg_7',
]


def get_training_data():
    """
    Return (X, y, daily_df_with_features) siap dipakai training.
    Baris awal yang fitur lag/rolling-nya masih NaN (karena belum ada
    histori sebelumnya) dibuang.
    """
    daily = get_daily_revenue_df()
    if daily.empty:
        return None, None, daily

    featured = add_features(daily)
    featured_clean = featured.dropna(subset=FEATURE_COLUMNS).reset_index(drop=True)

    X = featured_clean[FEATURE_COLUMNS]
    y = featured_clean['revenue']
    return X, y, featured
