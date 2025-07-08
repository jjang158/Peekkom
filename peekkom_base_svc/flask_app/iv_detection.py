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
    file.seek(0)
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Step 1: Segmentation 모델로 수액 여부 확인 및 crop
    seg_results = seg_model(img)

    # segmentation 모델에서 bounding box는 boxes로 접근
    if not seg_results or len(seg_results[0].boxes) == 0:
        return jsonify({"status": 'success', 'message': 'No IV bag detected in segmentation'}), 200

    # 첫 번째 탐지된 객체 기준으로 crop
    box = seg_results[0].boxes[0].xyxy[0].cpu().numpy()
    x1, y1, x2, y2 = map(int, box)
    cropped_image = img[y1:y2, x1:x2]

    # Step 2: Detection 모델로 전체 / 잔량 탐지
    det_results = det_model(cropped_image)

    iv_area = 0
    saline_area = 0

    if det_results and len(det_results[0].boxes) > 0:
        for box in det_results[0].boxes:
            cls_id = int(box.cls[0])
            label = det_model.names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
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
        send_fcm_notification(
            title='수액 부족 알림',
            body=f'수액 잔량이 {percent}%로 임계치보다 낮습니다!'
        )

    return jsonify({
        "status": 'success',
        "message" : f'iv_bag percent: {percent}',
        "detail" : {'iv_bag_area': iv_area,
                     'saline_level_area': saline_area,
                     'remaining_percent': percent,
                     'alert_sent': percent < THRESHOLD}
    }), 200
