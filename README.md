# aavail-ai-capstone
Capstone Submission

This Capstone is done in three parts, focusing on the forecasting. 

Part 1: data ingestion and transformation. Files are not consistent with regard to the column name. The data shows a clear seasonality. 
        The data also shows that not all invoice items are viewing, with some special charges. For forecasting purposes, we will only
        look that the invoice items for the streaming. 
Part 2: forecasting method. I took the approach of using Prophet, and specified a yearly seasonality. The forecasting error fitted for 
        the training data is around 5%. Reasonable. 
Part 3: test on the forecasting approach using the new data sets provided in cs-production. The forecast error for Aug/Sep is around 
        20~30%. The model had very good forecast for Oct/Nov at only 1~2%. But there is a cliff dropping on December, with forecast 
        at 595K and actual came in just at 220K. Upon further review, there are only 6 days of data from December, thus the big 
        forecasting error. 

Month 2019-08: Actual 435303.15000000014, Forecast 313353.5817118992, ERROR: 28.0%
Month 2019-09: Actual 631521.9500000001, Forecast 494700.7698733454, ERROR: 21.7%
Month 2019-10: Actual 751414.8600000007, Forecast 763186.3189682579, ERROR: 1.6%
Month 2019-11: Actual 936570.8500000004, Forecast 955371.4667877674, ERROR: 2.0%
Month 2019-12: Actual 220037.7600000002, Forecast 595207.1818298292, ERROR: 170.5%
MAE: 22.3%