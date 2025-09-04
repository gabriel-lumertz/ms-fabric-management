import requests
from dotenv import load_dotenv
import os

load_dotenv()

locatario_id = os.getenv("locatario_id")

URL_TOKEN = f"https://login.microsoftonline.com/{locatario_id}/oauth2/token"

BODY = {
    "client_id": os.getenv("client_id"),
    "grant_type": "client_credentials",
    "resource": "https://analysis.windows.net/powerbi/api",
    "client_secret": os.getenv("client_secret")
}


def get_token():
    response = requests.post(URL_TOKEN, data=BODY)
    response.raise_for_status()
    return response.json().get("access_token")


if __name__ == "__main__":
    token = get_token()
