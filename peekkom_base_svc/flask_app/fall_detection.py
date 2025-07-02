import cv2
from ultralytics import YOLO

# YOLO 모델 로드 (낙상자 탐지용으로 학습된 모델 경로)
model = YOLO("yolov8n.pt")  # 예: yolov8n.pt 또는 커스텀 모델

# 웹캠 열기
cap = cv2.VideoCapture(0)  # 0번 카메라

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 모델로 프레임 분석
    results = model(frame)

    # 결과 시각화
    annotated_frame = results[0].plot()

    # 낙상자 탐지 여부 확인
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            label = model.names[cls_id]

            # "fall"이라는 클래스를 감지했을 경우
            if label.lower() == "fall" and confidence > 0.5:
                print("[ALERT] 낙상자 감지됨!")
                # 이후 Flask API 호출 로직으로 연동 예정

    # 화면에 프레임 출력
    cv2.imshow("Fall Detection", annotated_frame)

    # 종료 조건: 'q' 키 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
