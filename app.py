# Bu kodun çalışması için bilgisayarınızda Python ve Flask kurulu olmalıdır.

import json
from flask import Flask, request, jsonify
from flask_cors import CORS 

app = Flask(__name__)
# CORS: Web sitenizin bu API'ye erişebilmesi için gereklidir.
CORS(app) 

# 1. Kulüp Veri Setini Yükleme Fonksiyonu
def load_club_data():
    """data.json dosyasını yükler."""
    try:
        # data.json dosyası app.py ile aynı klasörde olmalıdır
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("HATA: data.json dosyası bulunamadı! Lütfen kontrol edin.")
        return []

CLUB_DATA = load_club_data()

# 2. Öneri Sistemi Fonksiyonu (AI Mantığı: İçerik Tabanlı Eşleştirme)
def recommend_clubs_by_hobbies(user_hobbies):
    """
    Kullanıcı hobilerine göre kulüplere puan verir ve en uygun 3 tanesini önerir.
    """
    if not CLUB_DATA:
        return []

    club_scores = {}

    # Kullanıcının hobilerini küçük harfe çevirerek arama listesi oluştur
    search_hobbies = [h.lower() for h in user_hobbies]

    # Her kulübü değerlendir
    for club in CLUB_DATA:
        club_name = club['name']
        score = 0
        
        # Kulübün etiketlerini kontrol et
        for tag in club['tags']:
            # Eğer kulübün etiketi, kullanıcının hobileri arasında varsa puanı artır
            if tag.lower() in search_hobbies:
                score += 1 
        
        if score > 0:
            club_scores[club_name] = score

    # Puanlara göre kulüpleri sırala (En yüksek puanlı 3 kulübü al)
    # item: item[1] puanı temsil eder.
    sorted_clubs = sorted(club_scores.items(), key=lambda item: item[1], reverse=True)
    
    # Sadece kulüp isimlerini döndür
    top_recommendations = [name for name, score in sorted_clubs[:3]] 
    
    return top_recommendations

# 3. API Rotası
@app.route('/recommend', methods=['GET'])
def get_recommendations():
    # URL'den 'hobbies' (hobiler) parametrelerini bir liste olarak al
    user_hobbies = request.args.getlist('hobbies')
    
    if not user_hobbies:
        # Hobi bilgisi gelmezse, en popüler/genel kulüpleri varsayılan olarak döndür
        return jsonify(["Yazılım ve Teknoloji Kulübü", "Müzik ve Performans Kulübü"]), 200

    # AI/Öneri fonksiyonunu çağır
    recommendations = recommend_clubs_by_hobbies(user_hobbies)
    
    # Sonucu JSON formatında döndür
    return jsonify(recommendations), 200

if __name__ == '__main__':
    # API'yi yerel makinenizde (localhost) 5000 portunda çalıştır
    print("API sunucusu başlatılıyor. Lütfen bekleyin...")
    app.run(debug=True, port=5000)

# YENİ KISIM (Render/Gunicorn İçin)
if __name__ == '__main__':
    # Geliştirme için localde 5000 portunda çalıştır
    app.run(debug=True, port=5000)