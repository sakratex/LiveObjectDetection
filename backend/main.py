from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket
from models import Detection
import storage
from detection import detect_objects
from websocket_manager import WebSocketManager

app = FastAPI(
    title="Nesne Tespiti API",
    description="YOLO ile tespit edilen nesnelerin listelendiği API",
    version="1.0.0"
)

ws_manager = WebSocketManager()

@app.get("/")
def home():
    return {"message": "Nesne Tespiti API'ye hoş geldiniz!"}

@app.post("/detected-objects")
async def post_detection(detection: Detection):
    storage.add_detection(detection)
    await ws_manager.broadcast({"detections": [detection.dict()]})
    return {"message": "Tespit başarıyla kaydedildi", "data": detection}

@app.get("/detected-objects")
def get_all():
    return storage.get_all_detections()

@app.get("/detected-objects/latest")
def get_latest():
    latest = storage.get_latest_detection()
    if not latest:
        raise HTTPException(status_code=404, detail="Henüz veri yok.")
    return latest

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    image_bytes = await file.read()
    detections = detect_objects(image_bytes)
    
    if detections:
        await ws_manager.broadcast({"detections": detections})  
    return {"detections": detections}

#  WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        ws_manager.disconnect(websocket)
