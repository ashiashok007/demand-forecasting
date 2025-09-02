# Dataset Schema for Online Pharmacy Demand Forecasting

| Column                 | Type     | Description                                                     |
|------------------------|----------|-----------------------------------------------------------------|
| date                   | date     | Transaction date                                                |
| store_id (pharmacy_id) | string   | Partner pharmacy identifier                                     |
| prescription_id        | string   | Unique prescription upload ID                                   |
| prescription_flag      | binary   | 1 if placed via prescription upload, else 0                     |
| product_id             | string   | Medicine code                                                   |
| product_category       | string   | e.g. OTC, Prescription, Supplement                              |
| manufacturer           | string   | Company name                                                    |
| units_sold             | integer  | Number of units sold                                            |
| price                  | float    | Retail price per unit                                           |
| discount_percent       | float    | Discount applied (0–100)                                        |
| promotion_flag         | binary   | 1 if under promotion, else 0                                    |
| expiry_date            | date     | Medication expiry date                                          |
| inventory_level        | integer  | On-hand units before sale                                       |
| safety_stock           | integer  | Minimum buffer stock                                            |
| reorder_point          | integer  | Stock threshold for reordering                                  |
| order_quantity         | integer  | Quantity ordered from supplier                                  |
| lead_time_days         | integer  | Supplier lead time in days                                      |
| stock_out_flag         | binary   | 1 if units_sold > inventory_level, else 0                       |
| holiday_flag           | binary   | 1 if a public holiday, else 0                                   |
| special_event_flag     | binary   | 1 for festivals or epidemic alerts, else 0                     |
| delivery_time_hours    | float    | Hours from order to delivery                                    |
| delivery_delay_flag    | binary   | 1 if delivery_time_hours > SLA, else 0                          |
| competitor_price_index | float    | Price ratio vs. market average                                  |
| customer_segment_id    | string   | e.g. retail, wholesale                                          |
| day_of_week            | integer  | 0=Sunday…6=Saturday                                             |
| month_of_year          | integer  | 1=Jan…12=Dec                                                    |
