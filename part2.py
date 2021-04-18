"""
1. State the different modeling approaches that you will compare to address the business opportunity.

    Machine learning models such as random forest, regression with engieered features such as previous month(s). 

2. Iterate on your suite of possible models by modifying data transformations, pipeline architectures, hyperparameters and other relevant factors.

3. Re-train your model on all of the data using the selected approach and prepare it for deployment.

4. Articulate your findings in a summary report.
    The time series based on stream viewing shows a yearly seasonal pattern. The Prophet model gets about 5% MAE, which is reasonable. 

"""

from prophet import Prophet
import pandas as pd
from datetime import date, timedelta
from matplotlib import pyplot


def get_forecast(df_ts): 
    df_month = df_ts.groupby('inv_month').sum().reset_index()
    df_ts['inv_date'] = pd.to_datetime(df_ts['inv_date'])
    
    df_ts.rename(columns={'inv_date':'ds', 'value':'y'}, inplace=True)
    m = Prophet(yearly_seasonality=20)
    m.fit(df_ts)
    future = m.make_future_dataframe(periods=180, freq='D')
    forecast = m.predict(future)
    forecast['inv_month'] = forecast['ds'].apply(lambda v: date(v.year, v.month, 1).isoformat())
    monthly_forecast = forecast[['inv_month', 'yhat']].groupby('inv_month').sum().reset_index()

    df = pd.merge(monthly_forecast, df_month, on='inv_month', how='left')
    return df

if __name__ == "__main__":
    df_ts = pd.read_csv(r'cs-train\ts_data.csv')
    df = get_forecast(df_ts)
    df.to_csv(r'cs-train\forecasts.csv', index=False)


