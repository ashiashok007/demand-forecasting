# Feature Engineering Plan

This document outlines derived features to create from the synthetic dataset for the demand forecasting model.

1. Lag Features  
   - units_sold_lag_1: sales 1 day prior  
   - units_sold_lag_7: sales 7 days prior  

2. Rolling Window Statistics  
   - units_sold_roll_mean_7: 7-day moving average  
   - units_sold_roll_std_7: 7-day moving standard deviation  

3. Time-to-Expiry  
   - days_to_expiry: expiry_date – date  

4. Time Since Last Sale  
   - days_since_last_sale: days since the previous sale for each (store_id, product_id)  

5. Categorical Encodings  
   - One-hot encode product_category  
   - One-hot encode customer_segment_id  

6. Date-Derived Variables  
   - is_weekend: 1 if Saturday or Sunday, else 0  
   - day_of_month: day component of date  
   - quarter_of_year: fiscal quarter (1–4)  

7. Promotion Intensity  
   - promotion_intensity: normalized discount_percent (discount_percent / 100)  

8. Supply Chain Ratios  
   - order_to_sale_ratio: order_quantity / (units_sold + 1)  
   - lead_time_adjusted: lead_time_days × delivery_delay_flag  
