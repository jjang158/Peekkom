import firebase_admin
from firebase_admin import credentials, messaging

def send_fcm_notification(title, body):
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-adminsdk.json")
        firebase_admin.initialize_app(cred)

    // TODO - Device token 처리 변경
    message = messaging.Message(
        token='djeqyyhDSjet53TcMH_8g0:APA91bEqU6f5kwwwq9tXx6CZO-k5kPZ2guDccLblrUlD4XuXdzR9axmOw37c6QOoWJTvfA3jkT67P5PeM1n0p6Wn03U2WKVkWB7DxvnDTWcWVXWePpL3lfE',
        notification=messaging.Notification(
            title=title,
            body=body
        ),
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)
    return response
