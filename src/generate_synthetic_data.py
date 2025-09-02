import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid

def generate_synthetic_data(
    start_date='2025-01-01',
    end_date='2025-12-31',
    num_stores=5,
    num_products=20,
    num_records=10000
):
    # Date range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    # Generate random records
    data = []
    for _ in range(num_records):
        date = pd.to_datetime(np.random.choice(dates)).to_pydatetime()
        store_id = f"store_{np.random.randint(1, num_stores+1)}"
        prescription_id = str(uuid.uuid4())
        prescription_flag = np.random.choice([0, 1], p=[0.7, 0.3])
        product_id = f"prod_{np.random.randint(1, num_products+1)}"
        product_category = np.random.choice(['OTC', 'Prescription', 'Supplement'])
        manufacturer = np.random.choice(['Pfizer', 'Sun Pharma', 'Novartis'])
        units_sold = np.random.poisson(lam=5) + 1
        price = round(np.random.uniform(5.0, 100.0), 2)
        discount_percent = round(np.random.choice([0,10,20,30,50]), 2)
        promotion_flag = int(discount_percent > 0)
        expiry_date = date + timedelta(days=np.random.randint(30, 365))
        inventory_level = np.random.randint(0, units_sold + 20)
        safety_stock = np.random.randint(10, 30)
        reorder_point = safety_stock + np.random.randint(5, 20)
        order_quantity = np.random.randint(30, 100)
        lead_time_days = np.random.randint(1, 14)
        stock_out_flag = int(units_sold > inventory_level)
        holiday_flag = int(date.weekday() in [5, 6])  # weekend as proxy
        special_event_flag = int(np.random.rand() < 0.05)
        delivery_time_hours = round(np.random.normal(loc=24, scale=5), 2)
        delivery_delay_flag = int(delivery_time_hours > 48)
        competitor_price_index = round(np.random.uniform(0.8, 1.2), 2)
        customer_segment_id = np.random.choice(['retail', 'wholesale'])
        day_of_week = date.weekday()
        month_of_year = date.month

        data.append({
            'date': date,
            'store_id': store_id,
            'prescription_id': prescription_id,
            'prescription_flag': prescription_flag,
            'product_id': product_id,
            'product_category': product_category,
            'manufacturer': manufacturer,
            'units_sold': units_sold,
            'price': price,
            'discount_percent': discount_percent,
            'promotion_flag': promotion_flag,
            'expiry_date': expiry_date,
            'inventory_level': inventory_level,
            'safety_stock': safety_stock,
            'reorder_point': reorder_point,
            'order_quantity': order_quantity,
            'lead_time_days': lead_time_days,
            'stock_out_flag': stock_out_flag,
            'holiday_flag': holiday_flag,
            'special_event_flag': special_event_flag,
            'delivery_time_hours': delivery_time_hours,
            'delivery_delay_flag': delivery_delay_flag,
            'competitor_price_index': competitor_price_index,
            'customer_segment_id': customer_segment_id,
            'day_of_week': day_of_week,
            'month_of_year': month_of_year
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_synthetic_data()
    df.to_csv("data/synthetic_data.csv", index=False)
    print("Synthetic data generated at data/synthetic_data.csv")
