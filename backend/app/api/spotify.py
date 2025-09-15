import requests

def request_api(url, headers):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {
            "error": response.reason,
            "status": response.status_code,
        }, response.status_code

    data = response.json()
    return data
