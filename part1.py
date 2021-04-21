"""
(1) Assimilate the business scenario and articulate testable hypotheses:

    Create a machine learning model that predict a reasonable value for next month's revenue based on history
    
(2) State the ideal data to address the business opportunity and clarify the rationale for needing specific data.

    Monthly revenue data, and attributes that may contribute to the forecasting

(3) Create a python script to extract relevant data from multiple data sources, automating the process of data ingestion.

    Done

(4) Investigate the relationship between the relevant data, the target and the business metric.

    The revenue comes predominantly from UK and shows seasonality with peak in Q4

(5) Articulate your findings using a deliverable with visualizations.

    Done

"""

import os
import json
import time
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import altair as alt

def convert_to_ts(data_dir, df_orig, clean=False): 
    """Convert data to time series

    Args:
        df_orig (dataframe): dataframe form loading the data
    """

    output_file = os.path.join(data_dir, "ts_data.csv")
    if not clean and os.path.isfile(output_file):
        return pd.read_csv(output_file) 

    df_orig['s_type'] = df_orig['stream_id'].apply(lambda v: 'stream' if v[:5].isdigit() else 'other')
    df_orig = df_orig[df_orig['s_type'] == 'stream'].copy()
    df_orig['value'] = df_orig['times_viewed']*df_orig['price']
    df_orig['inv_date'] = df_orig.apply(lambda r: date(int(r['year']), int(r['month']), int(r['day'])), axis=1)
    df_orig['inv_month'] = df_orig.apply(lambda r: date(int(r['year']), int(r['month']), 1), axis=1)
    df_month = df_orig[['country', 'inv_month', 'value', 'times_viewed']].groupby(['country', 'inv_month']).sum().reset_index()
    
    df_customers = df_orig[pd.notna(df_orig['customer_id'])][['country', 'customer_id', 'inv_month']].drop_duplicates()
    df_customers = df_customers.groupby(['country', 'inv_month']).count().reset_index().rename(columns={'customer_id':'customers'})
    df_month = pd.merge(df_month, df_customers, how='left', on=['country', 'inv_month'])
    df_month.to_csv(os.path.join(data_dir, "ts_month_data.csv"), index=False)
    
    df_ts = df_orig[['country', 'inv_month', 'inv_date', 'value', 'times_viewed']].groupby(['country', 'inv_month', 'inv_date']).sum().reset_index()
    df_ts.to_csv(output_file, index=False)

    return df_ts

def fetch_ts(data_dir, clean=False):
    """Load data from json files

    Args:
        data_dir (string): directory where the json files reside
        clean (bool, optional): wheather to take a clean. Defaults to False.

    Returns:
        dataframe: combined data from the json files
    """

    output_file = os.path.join(data_dir, "combined_data.csv")
    if not clean and os.path.isfile(output_file):
        return pd.read_csv(output_file) 

    raw_dfs = []
    for file in [name for name in os.listdir(data_dir) if name[-4:]=='json']:
        f = open(os.path.join(data_dir, file))
        d = json.load(f)
        f.close()
        print(f".....loaded {len(d)} records from {os.path.join(data_dir, file)}")
        raw_dfs.append(pd.DataFrame(d).rename(columns={'total_price':'price', 'StreamID':'stream_id', 'TimesViewed':'times_viewed'}))
    
    df = pd.concat(raw_dfs)
    df.to_csv(output_file, index=False)
    return df

def visualize(df_ts, save_html=True):
    alt.Chart(df_ts).mark_line().encode(
        x=alt.X('inv_date:T', title='Invoice Date'),
        y=alt.Y('value:Q', title='Invoice Value'),
        row='country:N'
    ).properties(height=200, width=250, title=f'Daily Invoice Value for Countries').interactive().save(r"visuals\Daily Invoice Value for Countries.html")

    alt.Chart(df_ts).mark_line().encode(
        x=alt.X('inv_month:T', title='Invoice Month'),
        y=alt.Y('sum(value):Q', title='Invoice Value'),
        row='country:N'
    ).properties(height=200, width=250, title=f'Monthly Invoice Value for Countries').interactive().save(r"visuals\Monthly Invoice Value for Countries.html")

    alt.Chart(df_ts).mark_line().encode(
        x=alt.X('inv_month:T', title='Invoice Month'),
        y=alt.Y('sum(value):Q', title='Invoice Value'),
    ).properties(height=200, width=250, title=f'Monthly Invoice Value for All Countries').interactive().save(r"visuals\Monthly Invoice Value for All Countries.html")


if __name__ == "__main__":
    
    clean = False
    
    run_start = time.time() 
    data_dir = os.path.join(".", "cs-train")
    print("...fetching data")
    df_all = fetch_ts(data_dir, clean=clean)
    print(f"...fetched {len(df_all)} records")

    print("...convert to time series")
    df_ts = convert_to_ts(data_dir, df_all, clean=clean)
    print(f"...created {len(df_ts)} time series records")

    m, s = divmod(time.time()-run_start,60)
    h, m = divmod(m, 60)
    print("load time:", "%d:%02d:%02d"%(h, m, s))

    visualize(df_ts, True)

    # fig, ax = plt.subplots()
    # ax.plot('inv_date', 'value', data=df_ts)
    # fig.autofmt_xdate()
    # plt.title("Daily Revenue Over Time")
    # plt.xlabel("Invoice Date")
    # plt.ylabel("Invoice Value")

    # plt.show()

    
