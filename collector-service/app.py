from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

IMAGE_ANALYSIS_URL = "http://image-analysis:80/frame"
FACE_RECOGNITION_URL = "http://face-recognition:80/frame"
SECTION_URL = "http://section:80/persons"
ALERT_URL = "http://alert:80/alerts"

@app.route("/frame", methods=["POST"])
def handle_frame():
    data = request.get_json(force=True)
    headers = {"Content-Type": "application/json"}

    logging.info(f"Received frame: {data}")

    image_analysis_result = None
    face_recognition_result = None

    try:
        ia_response = requests.post(IMAGE_ANALYSIS_URL, json=data, headers=headers, timeout=5)
        if ia_response.status_code == 200:
            image_analysis_result = ia_response.json()
            logging.info(f"ImageAnalysis result: {image_analysis_result}")

        fr_response = requests.post(FACE_RECOGNITION_URL, json=data, headers=headers, timeout=5)
        if fr_response.status_code == 200:
            face_recognition_result = fr_response.json()
            logging.info(f"FaceRecognition result: {face_recognition_result}")

        if image_analysis_result and "persons" in image_analysis_result:
            section_payload = {
                "timestamp": data.get("timestamp"),
                "section": data.get("section"),
                "event": data.get("event"),
                "persons": image_analysis_result["persons"],
                "frame_uuid": data.get("frame_uuid", ""),
                "extra-info": data.get("extra-info", "")
            }
            requests.post(SECTION_URL, json=section_payload, headers=headers, timeout=5)
            logging.info("Forwarded to Section service")

        if face_recognition_result and "known-persons" in face_recognition_result:
            alert_payload = {
                "timestamp": data.get("timestamp"),
                "section": data.get("section"),
                "event": data.get("event"),
                "known-persons": face_recognition_result["known-persons"],
                "image": data.get("image", ""), 
                "frame_uuid": data.get("frame_uuid", ""),
                "extra-info": data.get("extra-info", "")
            }
            requests.post(ALERT_URL, json=alert_payload, headers=headers, timeout=5)
            logging.info("Forwarded to Alert service")

    except Exception as e:
        logging.error(f"Error during forwarding: {e}")

    return jsonify({"status": "frame processed"}), 200

@app.route("/livenessProbe", methods=["GET"])
def liveness():
    return "alive", 200

@app.route("/readinessProbe", methods=["GET"])
def readiness():
    return "ready", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
