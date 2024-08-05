import requests
import time

while True:
    response = requests.get("https://buddhiai.onrender.com/query-response")
    print(response.status_code)
    time.sleep(600)