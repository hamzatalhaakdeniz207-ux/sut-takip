from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Başlangıç verileri (ESP32 veri göndermediğinde ekranda bunlar yazar)
sensor_data = {
    "sicaklik": 0.0,
    "akim": 0.0,
    "doluluk": 0.0
}

# 1. DOSYA YOLU: manifest.json dosyasını dışarı açar (Samsung logo için)
@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

# 2. VERİ GÜNCELLEME: ESP32 buraya veri gönderir
@app.route('/update', methods=['POST'])
def update():
    global sensor_data
    # ESP32'den gelen JSON verisini alıyoruz
    data = request.get_json()
    if data:
        sensor_data["sicaklik"] = data.get("sicaklik", sensor_data["sicaklik"])
        sensor_data["akim"] = data.get("akim", sensor_data["akim"])
        sensor_data["doluluk"] = data.get("doluluk", sensor_data["doluluk"])
        print(f"Yeni Veri Geldi: {sensor_data}")
        return {"status": "basarili"}, 200
    return {"status": "hata", "message": "veri yok"}, 400

# 3. ANA SAYFA: Senin o şık grafikli panelini açar
@app.route('/')
def index():
    return render_template('index.html', data=sensor_data)

if __name__ == '__main__':
    # Render veya yerel sunucu için uygun port ayarı
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

