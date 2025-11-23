from flask import Flask, request, jsonify
from flask_cors import CORS
import ddddocr
import base64

app = Flask(__name__)
CORS(app)

# 初始化 OCR 模型（單例，使用 CPU）
try:
    ocr = ddddocr.DdddOcr(show_ad=False, device='cpu')  # 強制 CPU
except Exception as e:
    print(f"OCR 模型初始化失敗: {e}")
    ocr = None

@app.route("/")
def index():
    return "OCR Server is running!"

@app.route("/ocr", methods=["POST"])
def recognize():
    if ocr is None:
        return jsonify({"error": "OCR 模型未初始化"}), 500

    try:
        data = request.json
        image_base64 = data.get("ImageBase64")
        if not image_base64:
            return jsonify({"error": "缺少 ImageBase64"}), 400

        image_bytes = base64.b64decode(image_base64)
        result = ocr.classification(image_bytes)
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    # 用單 worker，避免 segfault
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", port, app)
