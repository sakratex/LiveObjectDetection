# Model Rehberi

## Model Tanıtımı
`detect/globalprojob.pt` dosyasında saklanan Ultralytics YOLO tabanlı bir nesne tespiti modeli. Aşağıdaki sınıfları tanır:
- **bicak** (Bıçak)
- **telefon** (Telefon)
- **kalem** (Kalem)

## Çıktı Biçimi
Model, her tespit için aşağıdaki yapıda bir liste döner:
```json
[
  {
    "class": "Telefon",
    "confidence": 0.85
  },
  ...
]
```
- **class**: Tespit edilen nesnenin adı.  
- **confidence**: 0–1 arası güven skoru (en fazla iki ondalık hane ile yuvarlanır).

## Sınırlılıklar
- Sadece %50 üzeri (0.5) güven skoru filtrelenir.  
- Eğitim verisinin kalitesi ve çeşitliliği modele bağlıdır.  
- `globalprojob.pt` modeli kara kutu gibidir; iç ağırlıkları doğrudan okunamaz.

## Modeli Yeniden Eğitme
1. **Veri Toplama ve Etiketleme**  
   - YOLO formatında verileri etiketleyin.  
2. **Eğitim Komutu**  
   ```bash
   yolo detect train data=dataset.yaml model=detect/globalprojob.pt epochs=50 imgsz=640
   ```  
3. **Yeni Modeli Kaydetme**  
   - `runs/train/exp/weights/best.pt` dosyasını `detect/globalprojob.pt` olarak değiştirin.  
4. **Değerlendirme**  
   ```bash
   yolo detect val data=dataset.yaml model=detect/globalprojob.pt
