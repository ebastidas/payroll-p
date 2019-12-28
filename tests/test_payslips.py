import requests


def test_api_running():
    url = 'http://0.0.0.0:8080/api/v1'
    resp = requests.get(url)
    assert resp.status_code == 200
    print(resp.text)


def test_payslips_endpoint():
    url = 'http://0.0.0.0:8080/api/v1/payslips'
    resp = requests.get(url)
    assert resp.status_code == 200
    assert resp.json()["_links"]["self"]["title"] == "payslips"
    print(resp.text)
