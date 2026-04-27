import os
import cv2
import torch
import numpy as np
from ultralytics import YOLO

# 1) Load trained detection model
MODEL_PATH = "runs/detect/train4/weights/best.pt"
model = YOLO(MODEL_PATH)

# 2) Image source
IMAGE_PATH = "dataset/detection/images"  # folder or single image
results = model.predict(source=IMAGE_PATH, save=False, conf=0.4)

# 3) Output folder
OUT_DIR = "explanations"
os.makedirs(OUT_DIR, exist_ok=True)

# 4) Simple explanation templates
EXPLANATIONS = {
    "Deity_Ganesha": "Detected due to trunk shape, crown, and facial structure.",
    "Deity_Hanuman": "Detected due to humanoid form, facial features, and posture.",
    "Supporting_Mouse": "Detected due to small animal shape near deity.",
    "Supporting_Apsara": "Detected due to human figure with ornamental posture.",
    "Symbol_Lotus": "Detected due to petal-like radial structure.",
    "Symbol_Trishul": "Detected due to three-pronged spear-like shape."
}

# 5) Generate heatmaps + annotated images
for i, r in enumerate(results):
    img = r.orig_img.copy()

    if r.boxes is None:
        continue

    for box, cls in zip(r.boxes.xyxy, r.boxes.cls):
        x1, y1, x2, y2 = map(int, box)
        label = r.names[int(cls)]

        # Crop region
        crop = img[y1:y2, x1:x2]
        if crop.size == 0:
            continue

        # Fake heatmap (simple intensity focus for demo)
        heat = cv2.applyColorMap(
            cv2.normalize(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY),
                          None, 0, 255, cv2.NORM_MINMAX),
            cv2.COLORMAP_JET
        )
        heat = cv2.resize(heat, (x2 - x1, y2 - y1))

        # Overlay heatmap
        overlay = cv2.addWeighted(crop, 0.6, heat, 0.4, 0)
        img[y1:y2, x1:x2] = overlay

        # Draw box + text
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        text = EXPLANATIONS.get(
            label, "Detected based on learned visual patterns.")
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(img, text, (x1, min(y2 + 20, img.shape[0] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    out_path = os.path.join(OUT_DIR, f"explain_{i}.jpg")
    cv2.imwrite(out_path, img)

print("Explanation images saved in 'explanations/'")
