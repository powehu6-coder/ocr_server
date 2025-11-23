# ocr_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import ddddocr
import base64
import re

app = Flask(__name__)
CORS(app)

ocr = ddddocr.DdddOcr()

@app.route("/")
def index():
    return "OCR Server is running!"


def safe_eval(expr: str):
    """
    安全算式解析，只允許: 數字 + - * /
    避免 eval 安全風險
    """
    if not re.fullmatch(r"[0-9+\-*/ ]+", expr):
        raise ValueError("Unsafe expression")

    return eval(expr)


@app.route("/ocridentify_GeneralCAPTCHA", methods=["POST"])
def identify_general():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    img_base64 = data.get("ImageBase64")
    if not img_base64:
        return jsonify({"error": "ImageBase64 is required"}), 400

    try:
        img_bytes = base64.b64decode(img_base64)
        result = ocr.classification(img_bytes)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ocridentify_ArithmeticCAPTCHA", methods=["POST"])
def identify_arithmetic():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    img_base64 = data.get("ImageBase64")
    if not img_base64:
        return jsonify({"error": "ImageBase64 is required"}), 400

    try:
        img_bytes = base64.b64decode(img_base64)
        expression = ocr.classification(img_bytes)

        # 安全計算算式
        answer = safe_eval(expression)
        return jsonify({"result": str(answer)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
