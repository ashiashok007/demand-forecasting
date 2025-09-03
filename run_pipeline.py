import os
import pandas as pd
import joblib
from datetime import timedelta

# Paths
MODEL_PATH       = 'models/random_forest_model.joblib'
IMPUTER_PATH     = 'models/mean_imputer.joblib'
SYNTHETIC_PATH   = 'data/synthetic_data.csv'
NEW_DATA_PATH    = 'data/new_data.csv'
FORECASTS_PATH   = 'predictions/forecast.csv'

def generate_new_data():
    if not os.path.exists(NEW_DATA_PATH):
        df = pd.read_csv(SYNTHETIC_PATH, parse_dates=['date','expiry_date'])
        df['date'] = df['date'] - timedelta(days=365)
        df['expiry_date'] = df['expiry_date'] - timedelta(days=365)
        df.to_csv(NEW_DATA_PATH, index=False)
        print(f"Generated {NEW_DATA_PATH}")
    else:
        print(f"{NEW_DATA_PATH} already exists")

def engineer_features(df):
    df = df.sort_values(['store_id','product_id','date']).reset_index(drop=True)
    # Lags
    df['units_sold_lag_1'] = df.groupby(['store_id','product_id'])['units_sold'].shift(1)
    df['units_sold_lag_7'] = df.groupby(['store_id','product_id'])['units_sold'].shift(7)
    # Rolling stats
    df['units_sold_roll_mean_7'] = df.groupby(['store_id','product_id'])['units_sold'] \
                                     .transform(lambda x: x.shift(1).rolling(7, min_periods=1).mean())
    df['units_sold_roll_std_7'] = df.groupby(['store_id','product_id'])['units_sold'] \
                                    .transform(lambda x: x.shift(1).rolling(7, min_periods=1).std())
    # Days to expiry & since last sale
    df['days_to_expiry'] = (df['expiry_date'] - df['date']).dt.days
    df['days_since_last_sale'] = df.groupby(['store_id','product_id'])['date'] \
                                   .transform(lambda x: x.diff().dt.days)
    # Encodings
    df = pd.get_dummies(df, columns=['product_category','customer_segment_id'], drop_first=True)
    # Date features
    df['is_weekend'] = df['date'].dt.weekday.isin([5,6]).astype(int)
    df['day_of_month'] = df['date'].dt.day
    df['quarter_of_year'] = df['date'].dt.quarter
    # Supply chain ratios
    df['promotion_intensity'] = df['discount_percent'] / 100
    df['order_to_sale_ratio'] = df['order_quantity'] / (df['units_sold'] + 1)
    df['lead_time_adjusted'] = df['lead_time_days'] * df['delivery_delay_flag']
    return df

if __name__ == '__main__':
    # 1. Ensure predictions folder exists
    os.makedirs(os.path.dirname(FORECASTS_PATH), exist_ok=True)

    # 2. Generate new data (if needed)
    generate_new_data()

    # 3. Load data, model, and imputer
    raw_df = pd.read_csv(NEW_DATA_PATH, parse_dates=['date','expiry_date'])
    model   = joblib.load(MODEL_PATH)
    imputer = joblib.load(IMPUTER_PATH)

    # 4. Feature engineering
    df_eng = engineer_features(raw_df)

    # 5. Select and impute features
    feature_cols = [
        'prescription_flag','price','discount_percent','promotion_flag',
        'inventory_level','safety_stock','reorder_point','order_quantity',
        'lead_time_days','stock_out_flag','holiday_flag','special_event_flag',
        'delivery_time_hours','delivery_delay_flag','competitor_price_index',
        'day_of_week','month_of_year','units_sold_lag_1','units_sold_lag_7',
        'units_sold_roll_mean_7','units_sold_roll_std_7','days_since_last_sale',
        'product_category_Prescription','product_category_Supplement',
        'customer_segment_id_wholesale','is_weekend','day_of_month',
        'quarter_of_year','promotion_intensity','order_to_sale_ratio',
        'lead_time_adjusted'
    ]
    X_new = df_eng[feature_cols]
    X_imputed_new = pd.DataFrame(imputer.transform(X_new),
                                 columns=feature_cols,
                                 index=X_new.index)

    # 6. Predict and save
    df_eng['forecast_units_sold'] = model.predict(X_imputed_new)
    df_eng[['store_id','product_id','date','forecast_units_sold']] \
          .to_csv(FORECASTS_PATH, index=False)
    print(f"Forecasts saved to {FORECASTS_PATH}")

