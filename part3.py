import os
import json
import time
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from prophet import Prophet

from part1 import fetch_ts, convert_to_ts

def get_forecast(df_ts, month): 
    
    actual = df_ts[df_ts['inv_month'] == month.isoformat()]['value'].sum()
    
    df_train = df_ts[df_ts['inv_month'] < month.isoformat()]
    df_train['inv_date'] = pd.to_datetime(df_train['inv_date'])
    df_train.rename(columns={'inv_date':'ds', 'value':'y'}, inplace=True)

    m = Prophet(yearly_seasonality=20)
    m.fit(df_train)
    future = m.make_future_dataframe(periods=60, freq='D')
    df_forecast = m.predict(future)
    df_forecast['inv_month'] = df_forecast['ds'].apply(lambda v: date(v.year, v.month, 1).isoformat())
    forecast = df_forecast[df_forecast['inv_month'] == month.isoformat()]['yhat'].sum()
    
    return actual, forecast

def test_forecast(df_ts, df_hist):

    df_ts = pd.concat([df_hist, df_ts])
    df_ts.sort_values('inv_date', inplace=True)
    months = [date(2019, 8, 1), date(2019, 9, 1), date(2019, 10, 1), date(2019, 11, 1), date(2019, 12, 1)]

    forecasts = []
    for m in months:
        actual, forecast = get_forecast(df_ts, m)
        forecasts.append((m, actual, forecast))

    print(forecasts)

    cumu_actual = 0
    cumu_abs_error = 0
    for (m, actual, forecast) in forecasts: 
        print(f"Month {m.strftime('%Y-%m')}: Actual {actual:.2}, Forecast {forecast:.2}, ERROR: {abs(forecast-actual)/actual:.1%}")
        if m != date(2019, 12, 1):
            cumu_actual += actual
            cumu_abs_error += abs(forecast-actual)

    print(f"MAE: {cumu_abs_error/cumu_actual:.1%}")
    
    # print(df_ts.head())

if __name__ == "__main__":
    clean = False
    data_dir = 'cs-production'
    df_all = fetch_ts(data_dir, clean=clean)
    df_ts = convert_to_ts(data_dir, df_all, clean=clean)

    df_hist = pd.read_csv(r'cs-train\ts_data.csv')
    test_forecast(df_ts, df_hist)
