from flask import Flask, request, jsonify
import requests
from config import ANDROID_API_URL

app = Flask(__name__)

@app.route('/send_alert', methods=['POST'])
def send_alert():
    try:
        data = request.json
        print("낙상자 알림 요청 수신:", data)

        # Android 앱으로 POST 요청 전송
        payload = {
            "type": "fall_detected",
            "message": "낙상자가 감지되었습니다!",
            "timestamp": data.get("timestamp")
        }

        response = requests.post(ANDROID_API_URL, json=payload)
        print("Android 앱 응답:", response.status_code)

        return jsonify({"status": "success", "android_status": response.status_code}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


