import requests

BASE_URL = "http://localhost:8000"
USERNAME = "rahul"
PASSWORD = "rahul@luqtaai#pipeline"

def get_token():
    url = f"{BASE_URL}/auth/token"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    print("Token response:", response.status_code, response.text)
    response.raise_for_status()
    return response.json()["access_token"]

def test_insights(token):
    url = f"{BASE_URL}/insights"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    # print("Insights response:", response.status_code, response.text)
    print("Insights response:", response.status_code)
    if(response.status_code == 200):
        print("Insights api working perfectly")
    response.raise_for_status()

def test_visualization_insights(token):
    url = f"{BASE_URL}/visualization_insights"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    # print("Visualization Insights response:", response.status_code, response.text)
    print("Visualization Insights response:", response.status_code)
    if(response.status_code == 200):
        print("Visualization Insights api working perfectly")
    response.raise_for_status()

if __name__ == "__main__":
    token = get_token()
    test_insights(token)
    test_visualization_insights(token)