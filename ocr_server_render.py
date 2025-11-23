# ocr_server_render.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import ddddocr
import base64

app = Flask(__name__)
CORS(app)  # 允許所有來源跨域

ocr = ddddocr.DdddOcr()

@app.route("/")
def index():
    return "OCR Server is running on Render!"

@app.route("/ocr", methods=["POST"])
def ocr_endpoint():
    """
    接收 JSON:
    {
        "ImageBase64": "data:image/png;base64,..."
    }
    返回 JSON:
    {
        "result": "識別結果"
    }
    """
    try:
        data = request.get_json()
        image_base64 = data.get("ImageBase64", "")

        # 去掉 data:image/png;base64, 前綴（如果有）
        if ',' in image_base64:
            image_base64 = image_base64.split(",")[1]

        image_bytes = base64.b64decode(image_base64)
        result = ocr.classification(image_bytes)

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Render 自動使用 $PORT
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
