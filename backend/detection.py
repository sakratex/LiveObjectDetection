
from ultralytics import YOLO
from PIL import Image
import io

model = YOLO(".\detect\globalprojob.pt")  

class_mapping = {
    "bicak": "Bıçak",
    "telefon": "Telefon",
    "kalem": "Kalem"
}

def detect_objects(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    results = model(image)

    detections = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0].item())
            label = model.names[class_id]
            confidence = float(box.conf[0].item())

            if confidence >= 0.5:
                detections.append({
                    "class": class_mapping.get(label, label),
                    "confidence": round(confidence, 2)
                })

    return detections
