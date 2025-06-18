# Nesne Tespiti Backend API

Bu proje, FastAPI kullanarak kamera görüntüsünden algılanan nesneleri (bıçak, telefon, kalem) tespit eden ve bu verileri WebSocket ile frontend'e anlık ileten bir backend servisidir.

---

## Kurulum ve Çalıştırma

1. Projeyi klonlayın:
```bash
git clone <repo-url>
cd <repo-klasörü>

2. Gerekli paketleri yükleyin:
pip install -r requirements.txt

3.Uygulamayı başlatın:
uvicorn main:app --reload

WebSocket Endpoint:
URL ws://localhost:8000/ws