# Proje Mimarisi

Bu belge, Nesne Tespiti API uygulamasındaki ana bileşenleri ve veri akışını açıklar.

## Bileşenler

1. **HTTP API (FastAPI)**
   - Uygulamanın giriş noktasıdır.
   - `/detect`, `/detected-objects` ve `/detected-objects/latest` gibi endpoint’leri sunar.
2. **YOLO Nesne Tespiti Modülü**
   - `backend/detection.py` içinde tanımlıdır.
   - Ultralytics YOLO modeli (`detect/globalprojob.pt`) kullanarak resimlerdeki nesneleri tespit eder.
3. **Depolama Katmanı**
   - `backend/storage.py` dosyasında bulunur.
   - Tespit edilen verileri bellekte liste halinde saklar.
   - `add_detection()`, `get_all_detections()`, `get_latest_detection()` fonksiyonlarını sağlar.
4. **WebSocket Yönetimi**
   - `backend/websocket_manager.py` içinde tanımlıdır.
   - Tespit gerçekleştiğinde bağlı tüm istemcilere anlık güncelleme gönderir.
   - `/ws` endpoint’i üzerinden çalışır.

## Veri Akış Diyagramı

```
İstemci
   │
   ├─ POST /detect (resim)
   │      ↓
API (FastAPI)
   │      ├─ detect_objects() → YOLO Modülü → tespitler
   │      ├─ storage.add_detection()
   │      └─ ws_manager.broadcast()
   │            ↓
   └─ WebSocket (anlık bildirim)
          ↓
     İstemci (güncel tespitler)
```

## Bileşenler Arası Etkileşim

1. İstemci, `/detect` uç noktasına resim gönderir.  
2. API, `detect_objects` fonksiyonunu çağırır ve sonuçları alır.  
3. Tespit sonuçları önce depolama katmanına eklenir, ardından WebSocket üzerinden yayınlanır.  
4. Başka bir istemci ya da uygulama, `/detected-objects` endpoint’i üzerinden geçmiş tespitleri alabilir veya `/ws` üzerinden gerçek zamanlı veri akışına abone olabilir.
