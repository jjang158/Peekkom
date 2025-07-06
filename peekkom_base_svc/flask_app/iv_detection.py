from flask import request, jsonify
from ultralytics import YOLO
import numpy as np
import cv2
from datetime import datetime
from send_notification import send_fcm_notification

# 모델 로딩
seg_model = YOLO('../iv_detection/ivbag_iv_seg.pt')  # segmentation model
det_model = YOLO('../iv_detection/trained_ivbag_yolov8s.pt')  # detection model

THRESHOLD = 20  # 수액 잔량 알람 임계치 (%)

def check_ivbag(file):
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Step 1: Segmentation 모델로 수액 여부 확인 및 crop
    seg_results = seg_model(img)

    if len(seg_results.xyxy[0]) == 0:
        return jsonify({"status": 'success', 'message': 'No IV bag detected in segmentation'}), 200

    # 첫 번째 탐지된 객체 기준으로 crop
    x1, y1, x2, y2 = map(int, seg_results.xyxy[0][0][:4])
    cropped_image = img[y1:y2, x1:x2]

    # Step 2: Detection 모델로 전체 / 잔량 탐지
    det_results = det_model(cropped_image)

    iv_area = 0
    saline_area = 0

    for *box, conf, cls in det_results.xyxy[0]:
        label = det_model.names[int(cls)]
        x1, y1, x2, y2 = map(int, box)
        area = (x2 - x1) * (y2 - y1)

        if label == 'iv_bag':
            iv_area += area
        elif label == 'saline_level':
            saline_area += area

    if iv_area == 0:
        return jsonify({"status": 'success', 'message': 'No iv_bag detected'}), 200

    percent = round((saline_area / iv_area) * 100, 2)

    # 알림 처리
    if percent < THRESHOLD:
        body = {
            "type": "fall_detected",
            "timestamp": datetime.now().isoformat(),
            "message": f'수액 잔량이 {percent}%로 임계치보다 낮습니다!'
        }
        send_fcm_notification(
            title='수액 부족 알림',
            body=body
        )

    return jsonify({
        'iv_bag_area': iv_area,
        'saline_level_area': saline_area,
        'remaining_percent': percent,
        'alert_sent': percent < THRESHOLD
    })
