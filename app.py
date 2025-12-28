from flask import Flask, render_template, request

app = Flask(__name__)

# 1. Buraya 'akim' bilgisini ekledik (Hafızada yer açtık)
data = {
    "sicaklik": 0,
    "akim": 0, 
    "durum": "Sistem Bekleniyor..."
}

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/guncelle', methods=['POST'])
def guncelle():
    gelen_veri = request.get_json()
    
    # 2. ESP32'den gelen paketin içindeki 'sicaklik' ve 'akim'ı alıyoruz
    data['sicaklik'] = gelen_veri.get('sicaklik', 0)
    data['akim'] = gelen_veri.get('akim', 0) 
    data['durum'] = gelen_veri.get('durum', "Aktif")
    
    print(f"Yeni Veri Geldi -> Sicaklik: {data['sicaklik']}, Akim: {data['akim']}")
    return {"status": "success"}

if __name__ == '__main__':
    app.run(debug=True)

    
