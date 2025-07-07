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
    fall_response, _ = detect_fall(file)
    fall_msg = fall_response.get_json().get("message")

    # 링거 확인
    iv_response, _ = check_ivbag(file)
    iv_msg = iv_response.get_json().get("message")

    return jsonify({
        "status": "success",
        "filename": file.filename,
        "fall_detection": fall_msg,
        "iv_check": iv_msg
    }), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

