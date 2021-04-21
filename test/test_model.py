from pytest import raises, approx
import os
import pandas as pd
from part2 import get_forecast


def test_logging():

    df_ts = pd.read_csv(r'..\cs-train\ts_data.csv')
    df = get_forecast(df_ts)

    assert "yhat" in df.columns