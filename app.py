import streamlit as st
import random

# 1. SAYFA AYARLARI VE TASARIM
st.set_page_config(page_title="5. Sınıf Pro Paneli", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #001C30; }
    .quiz-header { display: flex; justify-content: space-around; align-items: center; background-color: #1a3a5a; padding: 12px; border-radius: 12px; color: white; margin-bottom: 15px; }
    .score-badge { padding: 5px 15px; border-radius: 20px; font-weight: bold; min-width: 40px; text-align: center; }
    .correct-bg { background-color: #4CAF50; }
    .wrong-bg { background-color: #F44336; }
    .question-box { background-color: white; color: black; padding: 25px; border-radius: 10px; font-size: 18px; line-height: 1.6; border-left: 8px solid #2196F3; margin-bottom: 15px; }
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    .cat-card button { background-color: #FF8A80 !important; color: #102A43 !important; height: 80px !important; margin-bottom: 10px; }
    .test-card { background-color: #8BC34A; border-radius: 20px; padding: 15px; margin-bottom: 10px; color: #102A43; }
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; z-index: 1000; border-top: 1px solid #ccc; }
    </style>
    """, unsafe_allow_html=True)

# 2. GERÇEK MÜFREDAT VE SORU BANKASI SİSTEMİ
DERS_HAVUZU = {
    "Matematik": ["Doğal Sayılar", "Milyonlar", "Örüntüler", "Toplama Çıkarma", "Zihinden İşlemler"],
    "Türkçe": ["Sözcükte Anlam", "Kök ve Ekler", "Noktalama İşaretleri", "Yazım Kuralları"],
    "Fen Bilimleri": ["Güneş'in Yapısı", "Ay'ın Yapısı", "Ay'ın Evreleri", "Dünya'nın Hareketi"],
    "Sosyal Bilgiler": ["Haklarımı Öğreniyorum", "Çocuk Hakları", "Kültürel Miras"],
    "İngilizce": ["Hello!", "My Town", "Games and Hobbies"],
    "Din Kültürü": ["Allah İnancı", "Ramazan ve Oruç", "Nezaket Kuralları"]
}

# Her soru için benzersiz içerik üreten fonksiyon
def soru_olustur(ders, unite, soru_no):
    # Bu kısım her soru numarası için farklı şıklar ve metinler üretir
    random.seed(f"{ders}_{unite}_{soru_no}") # Soruların her zaman aynı ama benzersiz gelmesini sağlar
    dogru_cevap = random.choice(["A", "B", "C", "D"])
    
    if ders == "Fen Bilimleri":
        soru_metni = f"<b>{unite}</b> konusu kapsamında hangisi doğrudur?"
        if "Güneş" in unite: soru_metni = "Güneş ile ilgili bilgi edinmek için hangisi <u>uygun değildir</u>?"
    elif ders == "Matematik":
        sayi1, sayi2 = random.randint(10, 50), random.randint(10, 50)
        soru_metni = f"{sayi1} + {sayi2} işleminin sonucu aşağıdakilerden hangisidir?"
    else:
        soru_metni = f"{ders} dersi {unite} ünitesi {soru_no}. soru için hazırlanan yeni nesil sorudur."

    return {
        "soru": soru_metni,
        "A": "Cevap A şıkkıdır" if dogru_cevap == "A" else "Hatalı seçenek A",
        "B": "Cevap B şıkkıdır" if dogru_cevap == "B" else "Hatalı seçenek B",
        "C": "Cevap C şıkkıdır" if dogru_cevap == "C" else "Hatalı seçenek C",
        "D": "Cevap D şıkkıdır" if dogru_cevap == "D" else "Hatalı seçenek D",
        "cvp": dogru_cevap
    }

# 3. OTURUM YÖNETİMİ
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'stats' not in st.session_state: st.session_state.stats = {} # {test_key: {d:0, y:0, p:0}}
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'cevaplandi' not in st.session_state: st.session_state.cevaplandi = False

def navigate(to):
    st.session_state.page = to
    st.session_state.cevaplandi = False
    st.rerun()

# 4. SAYFALAR

# --- ANA SAYFA (image_10af63) ---
if st.session_state.page == 'home':
    st.markdown('<h2 style="color:white; text-align:center;">5. Sınıf Tüm Dersler</h2>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📝\nTestler"): navigate('kategoriler')
        st.button("🎬\nVideolar")
    with c2:
        st.button("❓\nRastgele")
        st.button("❤️\nFavori")
    with c3:
        st.button("📖\nKonu")
        st.button("📊\nİstatistik")
    st.button("🚫 Reklamları Kaldır", use_container_width=True)

# --- KATEGORİLER (image_10c1a5) ---
elif st.session_state.page == 'kategoriler':
    st.markdown('<h3 style="color:white;">KATEGORİLER</h3>', unsafe_allow_html=True)
    for ders in DERS_HAVUZU.keys():
        st.markdown('<div class="cat-card">', unsafe_allow_html=True)
        if st.button(f"📚 {ders} \n ✓ Kategori"):
            st.session_state.active_ders = ders
            navigate('test_listesi')
        st.markdown('</div>', unsafe_allow_html=True)

# --- TEST LİSTESİ (image_10c8ee / image_113664) ---
elif st.session_state.page == 'test_listesi':
    ders = st.session_state.active_ders
    st.markdown(f'<h3 style="color:white;">{ders} Testleri</h3>', unsafe_allow_html=True)
    
    for unite in DERS_HAVUZU[ders]:
        for i in range(1, 3): # Her üniteden 2 test
            t_key = f"{ders}_{unite}_{i}"
            s = st.session_state.stats.get(t_key, {"d": 0, "y": 0, "p": 0})
            st.markdown(f"""
                <div class="test-card">
                    <div style="font-weight:bold;">📋 {unite} Test {i}</div>
                    <div style="display:flex; justify-content:space-around; background:rgba(255,255,255,0.2); border-radius:10px; padding:5px; margin-top:5px; text-align:center;">
                        <div>20<br><small>SORU</small></div><div>{s['d']}<br><small>DOĞRU</small></div>
                        <div>{s['y']}<br><small>YANLIŞ</small></div><div>{s['p']}<br><small>PUAN</small></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Başlat: {unite} T{i}", key=t_key):
                st.session_state.active_unite = unite
                st.session_state.active_test_key = t_key
                st.session_state.q_idx = 0
                navigate('quiz')
    if st.button("⬅️ Geri Dön"): navigate('kategoriler')

# --- SORU EKRANI (image_1122ca / image_112a48) ---
elif st.session_state.page == 'quiz':
    ders = st.session_state.active_ders
    unite = st.session_state.active_unite
    idx = st.session_state.q_idx
    t_key = st.session_state.active_test_key
    
    if t_key not in st.session_state.stats: st.session_state.stats[t_key] = {"d":0, "y":0, "p":0}
    stats = st.session_state.stats[t_key]
    
    soru_verisi = soru_olustur(ders, unite, idx + 1)
    
    # Üst Gösterge Paneli
    st.markdown(f"""
        <div class="quiz-header">
            <span>⏰ 02:30</span>
            <span style="font-weight:bold;">{idx + 1} / 20</span>
            <span class="score-badge wrong-bg">{stats['y']}</span>
            <span class="score-badge correct-bg">{stats['d']}</span>
            <span>📝</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="question-box">{soru_verisi["soru"]}</div>', unsafe_allow_html=True)

    # Şıklar
    for h in ['A', 'B', 'C', 'D']:
        if st.button(f"{h}) {soru_verisi[h]}", key=f"ans_{h}_{idx}"):
            if not st.session_state.cevaplandi:
                if h == soru_verisi["cvp"]:
                    st.session_state.stats[t_key]["d"] += 1
                    st.session_state.stats[t_key]["p"] += 5
                    st.success("DOĞRU!")
                else:
                    st.session_state.stats[t_key]["y"] += 1
                    st.error(f"YANLIŞ! Doğru: {soru_verisi['cvp']}")
                st.session_state.cevaplandi = True

    # Navigasyon Butonları
    st.write("---")
    nb1, nb2, nb3, nb4 = st.columns(4)
    with nb1:
        if st.button("⬅️ Geri"):
            if st.session_state.q_idx > 0: st.session_state.q_idx -= 1; st.session_state.cevaplandi = False; st.rerun()
    with nb2: st.button("❤️")
    with nb3:
        if st.button("İleri ➡️"):
            if st.session_state.q_idx < 19: 
                st.session_state.q_idx += 1
                st.session_state.cevaplandi = False
                st.rerun()
            else: st.balloons(); navigate('test_listesi')
    with nb4:
        if st.button("❌"): navigate('test_listesi')

# SABİT ALT NAVİGASYON
st.write("<br><br><br>", unsafe_allow_html=True)
cols = st.columns(5)
with cols[0]:
    if st.button("🏠"): navigate('home')
with cols[1]:
    if st.button("📋"): navigate('kategoriler')
with cols[2]:
    st.button("📊")
with cols[3]:
    st.button("❤️")
with cols[4]:
    if st.button("◀️"): navigate('kategoriler')
