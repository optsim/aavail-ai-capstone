"""
1. State the different modeling approaches that you will compare to address the business opportunity.

    Machine learning models such as random forest, regression with engieered features such as previous month(s). 

2. Iterate on your suite of possible models by modifying data transformations, pipeline architectures, hyperparameters and other relevant factors.

3. Re-train your model on all of the data using the selected approach and prepare it for deployment.

4. Articulate your findings in a summary report.
    The time series based on stream viewing shows a yearly seasonal pattern. The Prophet model gets about 5% MAE, which is reasonable. 

"""

from prophet import Prophet
import json
from prophet.serialize import model_to_json, model_from_json
import pandas as pd
from datetime import date, timedelta
from matplotlib import pyplot
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt

def get_exp_forecast(df, country="ALL"): 
    df_ts = df.copy() if country=="ALL" else df[df['country']==country].copy()
    if len(df_ts) <= 180: 
        return None

    df_ts['inv_date'] = pd.to_datetime(df_ts['inv_date'])
    model = SimpleExpSmoothing(df_ts[['inv_month', 'inv_date', 'value']].set_index(['inv_month', 'inv_date'])).fit(smoothing_level=0.2, optimized=False)

    forecast_df = model.forecast(30).rename(r'value')
    return sum(forecast_df)

def get_prophet_forecast(df, country="ALL", save_model=True): 

    df_ts = df.copy() if country=="ALL" else df[df['country']==country].copy()
    if len(df_ts) <= 180: 
        return None

    df_month = df_ts.groupby('inv_month').sum().reset_index()
    df_ts['inv_date'] = pd.to_datetime(df_ts['inv_date'])
    
    df_ts.rename(columns={'inv_date':'ds', 'value':'y'}, inplace=True)
    m = Prophet(yearly_seasonality=20)
    m.fit(df_ts)
    
    if save_model: 
        with open(fr'models\{country}_model.json', 'w') as fout:
                json.dump(model_to_json(m), fout)  # Save model

    future = m.make_future_dataframe(periods=180, freq='D')
    forecast = m.predict(future)
    forecast['inv_month'] = forecast['ds'].apply(lambda v: date(v.year, v.month, 1).isoformat())
    monthly_forecast = forecast[['inv_month', 'yhat']].groupby('inv_month').sum().reset_index()

    df_forecast = pd.merge(monthly_forecast, df_month, on='inv_month', how='left')
    return df_forecast

if __name__ == "__main__":
    df_ts = pd.read_csv(r'cs-train\ts_data.csv')

    get_exp_forecast(df_ts)

    # df = get_prophet_forecast(df_ts)
    # df.to_csv(r'cs-train\forecasts.csv', index=False)

    # for country in df_ts['country'].drop_duplicates().to_list():
    #     get_prophet_forecast(df_ts, country)

