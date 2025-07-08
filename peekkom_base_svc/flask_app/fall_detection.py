from flask import jsonify
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import requests
import numpy as np
import cv2
from config import FALL_CONFIDENCE_THRESHOLD, UPLOAD_FOLDER
from send_notification import send_fcm_notification

# 모델 로드
model = YOLO("../fall_detection/fall_detection_v1.pt")

# 파일 업로드
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def detect_fall(file):
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # 이미지 분석
    results = model(img)
    fall_detected = False

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]
            if label == "fall" and conf > FALL_CONFIDENCE_THRESHOLD:
                fall_detected = True
                print(f"[ALERT] 낙상 감지 - confidence: {conf}")
                break

    # 결과에 따라 Android로 알림 전송
    if fall_detected:
        # 1. Android 앱 연동 (알림)
        try:
#             body = {
#                 "type": "fall_detected",
#                 "timestamp": datetime.now().isoformat(),
#                 "message":
#             }
            res = send_fcm_notification('낙상 감지', "낙상자가 감지되었습니다!")
            print(f"[INFO] Android 앱 응답 코드: {res}")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Android API 요청 실패: {e}")
            return jsonify({"status": 'error', "message": 'Android API 연동 실패'}), 502

        # 2. 낙상 이미지 저장
        try:
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
        except Exception as e:
            print(f"[ERROR] 이미지 저장 실패: {e}")
            return jsonify({"status": 'error', "message": '이미지 저장 실패'}), 500

    return jsonify({"status": 'success', 'message': f'fall_detected: {fall_detected}'}), 200
