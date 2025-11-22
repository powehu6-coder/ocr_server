# ocr_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import ddddocr
import base64

app = Flask(__name__)
CORS(app)

ocr = ddddocr.DdddOcr()

@app.route("/")
def index():
    return "OCR Server is running!"

@app.route("/ocridentify_GeneralCAPTCHA", methods=["POST"])
def identify_general():
    """
    接收 JSON:
    {
        "ImageBase64": "..."  # base64 圖片
    }
    回傳:
    {
        "result": "識別結果"
    }
    """
    data = request.get_json()
    img_base64 = data.get("ImageBase64", "")
    if not img_base64:
        return jsonify({"error": "no image"}), 400
    try:
        img_bytes = base64.b64decode(img_base64)
        result = ocr.classification(img_bytes)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ocridentify_ArithmeticCAPTCHA", methods=["POST"])
def identify_arithmetic():
    """
    對算式驗證碼做識別
    接收 JSON:
    {
        "ImageBase64": "..."
    }
    回傳:
    {
        "result": "答案"
    }
    """
    data = request.get_json()
    img_base64 = data.get("ImageBase64", "")
    if not img_base64:
        return jsonify({"error": "no image"}), 400
    try:
        img_bytes = base64.b64decode(img_base64)
        result = ocr.classification(img_bytes)
        # ddddocr 算式可以直接用 eval 計算
        answer = str(eval(result))
        return jsonify({"result": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
