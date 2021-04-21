
from pytest import raises, approx
import requests

def test_app_endpoint():
    url = 'http://127.0.0.1:8080/predict?date=2019-10-01'
    response = requests.get(url)
    obj = TrendDetector(env, data, 'Q')
    assert "month" in response.json()
    assert "forecast" in response.json()