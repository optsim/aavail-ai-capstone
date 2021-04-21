# aavail-ai-capstone
Capstone Submission

This Capstone is done in three parts, focusing on the forecasting. 

Part 1 

Data ingestion and transformation. Files are not consistent with regard to the column name. The data shows a clear seasonality. 
The data also shows that not all invoice items are viewing, with some special charges. For forecasting purposes, we will only
look that the invoice items for the streaming. The value of the invoice is the sum of products between the price of the stream, 
and # of views of the stream. While there are many countries in the datasets, there are only handful of countries that had 
consistent data. 

The visualizations with EDA are stored in visuals folder.  


Part 2

Forecasting method. I took the approach of using Prophet, and specified a yearly seasonality. The forecasting error fitted for 
the training data is around 5%. Reasonable. The forecast is made at the daily level, and then combined into monthly for 
reporting purposes. 

Also developed an exponential smoothing model to serve as coparison. 


Part 3

Test on the forecasting approach using the new data sets provided in cs-production. The forecast error for Aug/Sep is around 
20% to 30%. The model had very good forecast for Oct/Nov at only 2% to 4%. But there is a cliff dropping on December, with forecast 
at 595K and actual came in just at 220K. Upon further review, there are only 6 days of data from December, thus the big 
forecasting error. 

In constract, the exponential smoothing approach as the baseline model is significantly worse with regard to performance. 


Month 2019-08: Actual 4.4e+05, Forecast 3.2e+05, ERROR: 27.6%, EXP_ERROR: 150.0%

Month 2019-09: Actual 6.3e+05, Forecast 4.9e+05, ERROR: 21.9%, EXP_ERROR: 72.3%

Month 2019-10: Actual 7.5e+05, Forecast 7.8e+05, ERROR: 3.6%, EXP_ERROR: 44.8%

Month 2019-11: Actual 9.4e+05, Forecast 9.6e+05, ERROR: 2.8%, EXP_ERROR: 16.2%

Month 2019-12: Actual 2.2e+05, Forecast 5.9e+05, ERROR: 167.4%, EXP_ERROR: 394.6%

MAE: 11.3% vs. EXP MAE: 58.0%