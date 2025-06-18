from typing import List
from models import Detection

# Basit bir liste ile geçici veri saklıyoruz
detections: List[Detection] = []

def add_detection(detection: Detection):
    detections.append(detection)

def get_all_detections() -> List[Detection]:
    return detections

def get_latest_detection() -> Detection | None:
    if detections:
        return detections[-1]
    return None
