from flask import Flask, render_template, request

app = Flask(__name__)

# Verilerin tutulduğu sözlük - Virgüllere dikkat!
data = {
    "sicaklik": 0,
    "akim": 0.0,
    "durum": "Sistem Aktif"
}

@app.route('/')
def index():
    # Sitenin ana sayfasını açar ve verileri gönderir
    return render_template('index.html', data=data)

@app.route('/guncelle', methods=['POST'])
def guncelle():
    try:
        gelen_veri = request.get_json()
        if gelen_veri:
            # ESP32'den gelen verileri alıyoruz
            data['sicaklik'] = gelen_veri.get('sicaklik', data['sicaklik'])
            data['akim'] = gelen_veri.get('akim', data['akim'])
            data['durum'] = gelen_veri.get('durum', data['durum'])
            return {"status": "success"}, 200
        return {"status": "error", "message": "Veri yok"}, 400
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
    

