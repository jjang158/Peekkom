import firebase_admin
from firebase_admin import credentials, messaging

def send_fcm_notification(title, body):
#     load_dotenv()
#     fcm_key = os.getenv("FCM_SERVER_KEY")
#     device_token = os.getenv("DEVICE_TOKEN")
#     headers = {
#         'Authorization': f'key={fcm_key}',
#         'Content-Type': 'application/json',
#     }
#     payload = {
#         'to': device_token,
#         'notification': {
#             'title': title,
#             'body': body,
#         }
#     }
#     response = requests.post(FCM_API_URL, headers=headers, json=payload)
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-adminsdk.json")
        firebase_admin.initialize_app(cred)

    condition = "'stock-GOOG' in topics || 'industry-tech' in topics"
    message = messaging.Message(
        notification=messaging.Notification(
            title = title,
            body = body,
        ),
        condition=condition,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)
    return response
