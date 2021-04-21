# Import modules
from flask import Flask, request
import pandas as pd
from datetime import date
import json

from part3 import get_forecast
from part1 import fetch_ts, convert_to_ts

# Flask configuration
app = Flask(__name__)

@app.route("/")
def home():
    return "Revenue forecast!"

@app.route('/forecast', methods=['POST', 'GET'])
def forecast():
    data_dir = 'cs-production'
    df_all = fetch_ts(data_dir, clean=True)
    df_ts = convert_to_ts(data_dir, df_all, clean=True)
    df_hist = pd.read_csv(r'cs-train\ts_data.csv')
    df_ts = pd.concat([df_hist, df_ts])
    df_ts.sort_values('inv_date', inplace=True)

    m = date(request.get_json())
    _, forecast = get_forecast(df_ts, m)
    return json.dumps({"month":m, "forecast": forecast})
    

# Run app
if __name__ == '__main__':
    app.run()

# Start the server
# python -m flask run

