# Nesne Tespiti API

## Genel Bakış

Nesne Tespiti API, Ultralytics YOLO tabanlı nesne tespiti modeli kullanarak yüklenen resimlerdeki nesneleri tespit eder. FastAPI ve Pydantic ile oluşturulmuş bir HTTP API sunar. Tespit edilen nesneler depolama katmanına kaydedilir ve bağlı WebSocket istemcilerine anlık olarak iletilir. Otomatik ve interaktif dokümantasyon Swagger/OpenAPI üzerinden sunulur.

**Kullanılan Teknolojiler:**
- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- Ultralytics YOLO
- Pillow (PIL)
- WebSocket
- Custom `WebSocketManager`
- Nesne tespiti modeli (`detect/globalprojob.pt`)

## İnteraktif API Dokümantasyonu

Proje, FastAPI kullanılarak geliştirilmiş olup otomatik olarak `/docs` endpoint’inde interaktif Swagger/OpenAPI dokümantasyonu sunar.  
Bu dokümantasyona erişmek için:

```bash
uvicorn backend.main:app --reload
```

komutunu çalıştırın ve tarayıcınızdan `http://127.0.0.1:8000/docs` adresine gidin.

## Kurulum Rehberi

1. Depoyu klonlayın  
   ```bash
   git clone https://github.com/your-username/LiveObjectDetection.git
   cd LiveObjectDetection
   ```

2. Sanal ortam oluşturun (opsiyonel)  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Gerekli Python paketlerini yükleyin  
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Nesne tespiti modeli dosyasını indirin  
   - `detect/globalprojob.pt` dosyasını `detect/` klasörüne yerleştirin.

5. Ortam değişkenleri (varsa)  
   - `.env` dosyası oluşturarak gerekli değişkenleri ekleyin.

## Kullanım Kılavuzu

### Backend Sunucusunu Başlatma

```bash
uvicorn backend.main:app --reload
```

### API Örnekleri

- `/detect` endpoint’i ile resim yükleyerek nesne tespiti  
  ```bash
  curl -X POST "http://127.0.0.1:8000/detect" \
       -H "Content-Type: multipart/form-data" \
       -F "file=@path/to/image.jpg"
  ```

- Tespit edilen nesneleri kaydet  
  ```bash
  curl -X POST "http://127.0.0.1:8000/detected-objects" \
       -H "Content-Type: application/json" \
       -d '{"timestamp":"2025-06-20T12:00:00","objects":["Telefon","Kalem"]}'
  ```

- Kayıtlı tespitleri listele  
  ```bash
  curl "http://127.0.0.1:8000/detected-objects"
  ```

- En son tespiti al  
  ```bash
  curl "http://127.0.0.1:8000/detected-objects/latest"
  ```

### WebSocket

Nesne tespitleri anlık olarak WebSocket üzerinden yayınlanır. Bağlanmak için:

```bash
ws://127.0.0.1:8000/ws
```

### Frontend Arayüzü

Projeye dahil HTML ön yüzünü test etmek için:

- `frontend/index-2.html` dosyasını tarayıcıda açın.
