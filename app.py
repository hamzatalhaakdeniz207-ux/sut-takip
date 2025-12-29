from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Burası verilerin hafızada tutulduğu yer. 
# Gerçek veriler gelene kadar içinde örnek bir veri olsun.
tank_verileri = {
    "sicaklik": 4.0,
    "doluluk": 850,
    "durum": "Sogutma Aktif"
}

@app.route('/')
def ana_sayfa():
    # Templates klasöründeki index.html dosyasını çalıştırır
    # ve içindeki değişkenleri günceller.
    return render_template('index.html', veri=tank_verileri)

# ESP32 ileride bu adrese veri gönderecek
@app.route('/guncelle', methods=['POST'])
def guncelle():
    global tank_verileri
    yeni_gelen = request.get_json()
    tank_verileri.update(yeni_gelen)
    return jsonify({"mesaj": "Veri güncellendi"}), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    


