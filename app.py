from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Canlı verilerin tutulduğu sözlük
sensor_data = {"sicaklik": 0.0, "akim": 0.0, "doluluk": 0.0}

# ESP32 BURAYA VERİ GÖNDERİR
@app.route('/update', methods=['POST'])
def update():
    global sensor_data
    data = request.get_json()
    if data:
        sensor_data["sicaklik"] = data.get("sicaklik", sensor_data["sicaklik"])
        sensor_data["akim"] = data.get("akim", sensor_data["akim"])
        sensor_data["doluluk"] = data.get("doluluk", sensor_data["doluluk"])
        return {"status": "ok"}, 200
    return {"status": "error"}, 400

# WEB SİTESİ BURADAN ANLIK VERİ ÇEKER (Sayfa yenilemeden)
@app.route('/veriler')
def veriler():
    return jsonify(sensor_data)

# ANA SAYFAYI AÇAR
@app.route('/')
def index():
    return render_template('index.html', data=sensor_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
