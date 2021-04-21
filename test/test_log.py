
from pytest import raises, approx
import os
import pandas as pd

def test_logging():
    LOG_DIR = '..'
    LOG_FILE = 'prophet_forecast.log'

    assert os.path.join(LOG_DIR, LOG_FILE).isfile()
    df = pd.read_csv(os.path.join(LOG_DIR, LOG_FILE))
    
    assert ["Month", "Actual", "Forecast"] == df.columns