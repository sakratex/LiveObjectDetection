# API Kullanım Rehberi

## HTTP Senaryoları

### 1. Nesne Tespiti (`/detect`)
Resim dosyası göndererek nesne tespiti yapın:
```bash
curl -X POST "http://127.0.0.1:8000/detect" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/image.jpg"
```
Başarılı yanıtta JSON:
```json
{
  "detections": [
    { "class": "Telefon", "confidence": 0.92 },
    { "class": "Kalem", "confidence": 0.76 }
  ]
}
```

### 2. Tespit Verilerini Kaydetme (`/detected-objects`)
Elde edilen tespitleri uygulama veritabanına ekleyin:
```bash
curl -X POST "http://127.0.0.1:8000/detected-objects" \
     -H "Content-Type: application/json" \
     -d '{
           "timestamp": "2025-06-20T15:30:00",
           "objects": ["Telefon","Kalem"]
         }'
```

### 3. Tüm Kayıtlı Tespitleri Listeleme
```bash
curl "http://127.0.0.1:8000/detected-objects"
```

### 4. En Son Tespiti Getirme
```bash
curl "http://127.0.0.1:8000/detected-objects/latest"
```

## WebSocket Senaryosu

API, tespitler gerçekleştiğinde gerçek zamanlı bildirimler için WebSocket sunar.

### Bağlantı Kurma
JavaScript ile:
```javascript
const socket = new WebSocket("ws://127.0.0.1:8000/ws");

socket.addEventListener("open", () => {
  console.log("WebSocket bağlantısı kuruldu.");
});

socket.addEventListener("message", (event) => {
  const data = JSON.parse(event.data);
  console.log("Yeni tespitler:", data.detections);
});
```

### Mesaj Gönderme
Sunucu sürekli veri göndermek üzere tasarlandığından, göndereceğiniz mesaj içerik önemsenmez. Bağlandıktan sonra örneğin ping gönderebilirsiniz:
```javascript
socket.send("ping");
```

## Uygulama Örnek Akışı

1. `/detect` endpoint’ine JPEG/PNG resim yükleyin.  
2. Hemen JSON çıktısını alın ve ekranda gösterin.  
3. Aynı anda WebSocket üzerinden yeni tespitleri dinleyin ve gerçek zamanlı güncelliği sağlayın.  
4. Geçmiş tespitleri `/detected-objects` veya `/detected-objects/latest` ile sorgulayın.
