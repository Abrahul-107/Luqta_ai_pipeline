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
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        print("Token response:", response.status_code, response.text)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get token: {e}")
        return None


def test_insights(token):
    if not token:
        print("[SKIP] Skipping Insights API test (no token)")
        return
    url = f"{BASE_URL}/insights"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print("Insights response:", response.status_code)
        if response.status_code == 200:
            print("✅ Insights API working perfectly")
        else:
            print("⚠️ Insights API returned unexpected status:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Insights API failed: {e}")


def test_visualization_insights(token):
    if not token:
        print("[SKIP] Skipping Visualization Insights API test (no token)")
        return
    url = f"{BASE_URL}/visualization_insights"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print("Visualization Insights response:", response.status_code)
        if response.status_code == 200:
            print("✅ Visualization Insights API working perfectly")
        else:
            print("⚠️ Visualization Insights API returned unexpected status:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Visualization Insights API failed: {e}")


if __name__ == "__main__":
    token = get_token()
    test_insights(token)
    test_visualization_insights(token)
