# 빼곰(Peekkom)
UWC 2025 AI &amp; 무인이동체 퓨처 해커톤 
- 팀명 : A.IDLE
- 주요 서비스 : 환자 모니터링 서비스

## 프로젝트 개요

**Peekkom**은 인공지능 기반 환자 모니터링 시스템으로, 병원이나 요양시설 등에서 환자의 낙상이나 수액 부족 상황을 자동으로 감지하고, 실시간으로 보호자나 간호사에게 모바일 알림을 전송하는 서비스입니다. 이 프로젝트는 UWC AI & 무인동체 퓨처 해커톤에서 개발된 프로토타입으로, 환자의 안전을 강화하고 의료진의 부담을 줄이는 것을 목적으로 합니다.

Peekkom은 실시간으로 카메라 영상을 분석하여 낙상 여부나 수액 잔량을 확인하고, 이상 상황 발생 시 Android 앱으로 즉시 알림을 보내 응급 대응이 가능하도록 합니다. 병원, 요양시설, 가정 간호 등 다양한 환경에서 활용할 수 있습니다.

## 주요 기능

- **낙상 감지 기능**: YOLOv8 기반 컴퓨터 비전 모델을 사용하여 이미지에서 사람이 바닥에 쓰러져 있는 상황을 감지합니다. 낙상이 의심되면 즉시 알림을 전송합니다.

- **수액 잔량 모니터링**: IV 수액 백을 인식하고, 잔량이 설정된 임계치(기본 20%) 이하일 경우 수액 부족 알림을 전송합니다. AI 모델을 통해 수액 백과 잔량을 세분화하여 감지합니다.

- **모바일 실시간 알림 (FCM)**: Firebase Cloud Messaging을 활용해 Android 앱으로 실시간 푸시 알림을 보냅니다. 알림에는 발생한 이벤트와 관련된 설명, 시간 등이 포함됩니다.

- **Android 전용 앱**: Jetpack Compose 기반으로 개발된 Android 앱으로, 백그라운드에서 알림을 수신하고 UI에서 간단한 상태 확인 및 테스트 기능을 제공합니다.

- **이미지 업로드 및 로깅**: 웹 페이지나 API를 통해 이미지를 업로드하면, 해당 이미지를 분석한 후 결과를 리턴하고, 필요 시 이미지를 서버에 저장해 이력 관리도 가능하게 합니다.

## 기술 스택

- **언어 및 플랫폼**:

  - Kotlin (Android 앱)
  - Python (Flask 기반 백엔드)
  - Jupyter Notebook (모델 학습 기록)

- **Android 앱 기술**:

  - Jetpack Compose (UI)
  - Firebase Cloud Messaging (FCM 푸시 알림)

- **백엔드 기술**:

  - Flask (Python 웹 서버)
  - Ultralytics YOLOv8 (낙상/수액 모델)
  - OpenCV, NumPy, Requests, python-dotenv

- **머신러닝/딥러닝**:

  - YOLOv8 custom segmentation & detection 모델 (낙상 감지, 수액 백 탐지)
  - Roboflow 기반 수액 데이터셋 활용 및 커스텀 학습

## 설치 및 실행 방법

### 1. 레포지토리 클론

```bash
git clone https://github.com/moveho/Peekkom.git
cd Peekkom
```

### 2. 백엔드 서버 (Flask)

- Python 3.x 및 가상환경 권장
- 패키지 설치:

```bash
cd peekkom_base_svc/flask_app
pip install flask ultralytics opencv-python numpy requests python-dotenv
```

- 모델 가중치 파일이 필요합니다:

  - `iv_detection/ivbag_iv_seg.pt`
  - `iv_detection/trained_ivbag_yolov8s.pt`
  - `fall_detection/fall_detection_v1.pt`

- `.env` 파일 생성:

```
FCM_SERVER_KEY=발급받은 FCM 서버 키
DEVICE_TOKEN=Android 앱에서 출력된 토큰
```

- 서버 실행:

```bash
python app.py
```

기본 포트는 [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 3. Android 앱

- Android Studio로 `PeekkomApplication` 디렉토리 열기
- Firebase 프로젝트 생성 후 `google-services.json` 파일을 `app/` 디렉토리에 추가
- 앱 실행 후 Logcat에서 FCM 토큰을 확인하여 `.env`에 반영

## 사용 예시

- **이미지 업로드 테스트 (curl 사용)**

```bash
curl -X POST -F "image=@/경로/이미지.jpg" http://127.0.0.1:5000/upload
```

- 결과 예시:

```json
{
  "remaining_percent": 18.5,
  "alert_sent": true
}
```

- Android 기기에는 “수액 부족 알림” 또는 “낙상 감지”라는 알림이 실시간으로 전송됨

- **웹 인터페이스 테스트**: [http://127.0.0.1:5000](http://127.0.0.1:5000) 에서 직접 업로드 가능

- **앱 테스트 버튼**: “테스트 알림 보기” 버튼 클릭 시 임의의 수액 상태가 갱신됨 (실제 FCM과는 무관한 로컬 테스트용)

## 기여 가이드

1. Fork 및 브랜치 생성 후 작업 권장
2. 기능 개발 또는 버그 수정 후 Pull Request 요청
3. Python은 PEP8, Kotlin은 Android 스타일 가이드 준수
4. README 또는 문서 수정 필수 (기능 추가 시)
5. 이슈 등록 시 재현 방법, 스크린샷, 로그 포함 부탁드립니다

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

자유롭게 복제, 수정, 배포할 수 있으며, 저작권 및 라이선스 고지 포함 시 상업적 이용도 가능합니다. 

---


