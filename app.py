from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Başlangıç verileri - ESP32'den veri gelene kadar bunlar görünür
sensor_data = {
    "sicaklik": 0.0,
    "akim": 0.0,
    "doluluk": 0.0
}

# 1. DOSYA YOLU: Samsung telefonlarda logonun görünmesi için gerekli
@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

# 2. VERİ GÜNCELLEME (KRİTİK BÖLÜM): ESP32 tüm sensör verilerini buraya gönderir
@app.route('/update', methods=['POST'])
def update():
    global sensor_data
    # ESP32'den gelen 3'lü veri paketini (JSON) alıyoruz
    data = request.get_json()
    if data:
        # Gelen verileri tek tek ayıklayıp sisteme kaydediyoruz
        sensor_data["sicaklik"] = data.get("sicaklik", sensor_data["sicaklik"])
        sensor_data["akim"] = data.get("akim", sensor_data["akim"])
        sensor_data["doluluk"] = data.get("doluluk", sensor_data["doluluk"])
        
        print(f"Canlı Veri Geldi -> Sıcaklık: {sensor_data['sicaklik']} | Akım: {sensor_data['akim']} | Doluluk: {sensor_data['doluluk']}")
        return {"status": "basarili"}, 200
    return {"status": "hata", "message": "veri ulasmadi"}, 400

# 3. ANA SAYFA: Senin o şık grafikli panelini açan bölüm
@app.route('/')
def index():
    return render_template('index.html', data=sensor_data)

if __name__ == '__main__':
    # Render platformunun istediği port ayarı
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
