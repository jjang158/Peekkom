from flask import jsonify
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import requests
from config import ANDROID_API_URL, CONFIDENCE_THRESHOLD, UPLOAD_FOLDER

# 모델 로드
model = YOLO("../../fall_detection/fall_detection_v1.pt")

# 파일 업로드
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def detect_fall(file):
    # 이미지 분석
    results = model(file)
    fall_detected = False

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]
            if label == "fall" and conf > CONFIDENCE_THRESHOLD:
                fall_detected = True
                print(f"[ALERT] 낙상 감지 - confidence: {conf}")
                break

    # 결과에 따라 Android로 알림 전송
    if fall_detected:
        payload = {
            "type": "fall_detected",
            "timestamp": datetime.now().isoformat(),
            "message": "낙상 감지됨"
        }

        # 1. Android 앱 연동 (알림)
        try:
            res = requests.post(ANDROID_API_URL, json=payload)
            print(f"[INFO] Android 앱 응답 코드: {res.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Android API 요청 실패: {e}")
            return jsonify({'error': 'Android API 연동 실패'}), 502

        # 2. 낙상 이미지 저장
        try:
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
        except Exception as e:
            print(f"[ERROR] 이미지 저장 실패: {e}")
            return jsonify({'error': '이미지 저장 실패'}), 500

    return jsonify({'fall_detected': fall_detected})
