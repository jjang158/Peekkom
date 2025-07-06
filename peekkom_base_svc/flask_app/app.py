from flask import Flask, request, jsonify
from fall_detection import detect_fall
from iv_detection import check_ivbag

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'message': '이미지 파일이 없습니다.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'message': '선택된 파일이 없습니다.'}), 400

    # 낙상자 탐지
    detect_fall(file)

    # 링거 확인
    check_ivbag(file)

    return jsonify({"status": 'success', 'message': f'확인 완료: {file.filename}'}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

