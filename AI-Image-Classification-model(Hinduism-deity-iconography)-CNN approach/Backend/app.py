from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from correlation_engine import infer_deities
import os
import uuid

app = Flask(__name__)
CORS(app)

MODEL_PATH = "C:/Users/Boris Butelho/OneDrive/Desktop/runs/detect/train2/weights/best.pt"
model = YOLO(MODEL_PATH)


# ---------- Narrative Generator ----------
def generate_detailed_explanation(primary_deity, matched_clues, avg_confidence, associated_deities):

    text = []

    text.append(f"Primary Deity Identified: {primary_deity.capitalize()}\n")

    text.append(
        f"{primary_deity.capitalize()} is a central and highly revered figure in Hindu iconography. "
        "The structural composition of the image aligns with classical devotional "
        "representations traditionally associated with this deity."
    )

    text.append("\nIconographic Evidence Detected:")
    for clue in matched_clues.get(primary_deity, []):
        text.append(
            f"• {clue.replace('_', ' ').capitalize()} — This element is strongly associated "
            f"with {primary_deity.capitalize()}."
        )

    text.append("\nSymbolic Interpretation:")
    text.append(
        "The detected attributes represent deeper philosophical and theological principles "
        "within Hindu tradition."
    )

    text.append("\nCultural Context:")
    text.append(
        "Such representations are commonly found in temple sculptures, brass idols, "
        "and sacred devotional art across India."
    )

    text.append("\nSystem Confidence Assessment:")
    if avg_confidence >= 0.80:
        text.append(
            "High confidence identification based on multiple strong markers.")
    elif avg_confidence >= 0.55:
        text.append(
            "Moderate confidence identification with strong supporting evidence.")
    else:
        text.append("Identification based on partial visual cues.")

    text.append(
        f"\nFinal Determination: The figure is identified as {primary_deity.capitalize()}."
    )

    return "\n".join(text)


# ---------- API Endpoint ----------
@app.route("/analyze", methods=["POST"])
def analyze():

    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]

    temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
    file.save(temp_filename)

    results = model.predict(source=temp_filename, conf=0.25, save=False)

    detected_labels = []
    confidences = []

    for r in results:
        if r.boxes is None:
            continue
        for box in r.boxes:
            label = r.names[int(box.cls)]
            conf = float(box.conf)
            detected_labels.append(label)
            confidences.append(conf)

    os.remove(temp_filename)

    if not detected_labels:
        return jsonify({"message": "No objects detected"})

    # Remove duplicates, keep strongest confidence
    label_conf_map = {}
    for label, conf in zip(detected_labels, confidences):
        if label not in label_conf_map:
            label_conf_map[label] = conf
        else:
            label_conf_map[label] = max(label_conf_map[label], conf)

    detected_labels = list(label_conf_map.keys())
    avg_confidence = sum(label_conf_map.values()) / len(label_conf_map)

    scores, matched_clues = infer_deities(detected_labels)

    if not scores:
        return jsonify({"message": "No strong deity correlation found"})

    # Boost direct deity detection
    for label in detected_labels:
        if label in scores:
            scores[label] += 5

    sorted_deities = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary_deity = sorted_deities[0][0]

    explanation = generate_detailed_explanation(
        primary_deity,
        matched_clues,
        avg_confidence,
        sorted_deities
    )

    return jsonify({
        "primary_deity": primary_deity,
        "confidence": round(avg_confidence, 2),
        "detected_labels": detected_labels,
        "explanation": explanation
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
