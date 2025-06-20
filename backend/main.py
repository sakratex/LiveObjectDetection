from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .models import Detection
from . import storage
from .detection import detect_objects
from .websocket_manager import WebSocketManager

app = FastAPI(
    title="Nesne Tespiti API",
    description="YOLO ile tespit edilen nesnelerin listelendiği API",
    version="1.0.0"
)

# Statik frontend dosyalarını /static altında sun
app.mount("/static", StaticFiles(directory="frontend"), name="static")

ws_manager = WebSocketManager()

@app.get("/")
def home():
    # Ana sayfa olarak index-2.html döndür
    return FileResponse("frontend/index-2.html")

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
    # Kutuları ve etiketleri içeren tüm tespitleri yayınla
    await ws_manager.broadcast({"detections": detections})
    return {"detections": detections}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Gelen mesajı bekle ve görmezden gel
            await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        ws_manager.disconnect(websocket)
