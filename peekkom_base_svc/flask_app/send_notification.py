import requests
from config import FCM_API_URL
import os
from dotenv import load_dotenv

def send_fcm_notification(title, body):
    load_dotenv()
    fcm_key = os.getenv("FCM_SERVER_KEY")
    device_token = os.getenv("DEVICE_TOKEN")
    headers = {
        'Authorization': f'key={fcm_key}',
        'Content-Type': 'application/json',
    }
    payload = {
        'to': device_token,
        'notification': {
            'title': title,
            'body': body,
        }
    }
    response = requests.post(FCM_API_URL, headers=headers, json=payload)
    print('[FCM 응답]', response.status_code, response.text)
    return response
