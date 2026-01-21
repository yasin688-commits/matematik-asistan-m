import streamlit as st

# 1. SAYFA AYARLARI VE TASARIM
st.set_page_config(page_title="Akıllı Eğitim Paneli", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #001C30; }
    .quiz-header { display: flex; justify-content: space-around; align-items: center; background-color: #1a3a5a; padding: 12px; border-radius: 12px; color: white; margin-bottom: 15px; }
    .score-badge { padding: 5px 15px; border-radius: 20px; font-weight: bold; min-width: 40px; text-align: center; }
    .correct-bg { background-color: #4CAF50; }
    .wrong-bg { background-color: #F44336; }
    .question-box { background-color: white; color: black; padding: 25px; border-radius: 10px; font-size: 18px; line-height: 1.6; margin-bottom: 15px; border-left: 8px solid #2196F3; }
    .stButton>button { width: 100%; border-radius: 12px; height: 55px; font-weight: bold; }
    .cat-card button { background-color: #FF8A80 !important; color: #102A43 !important; height: 80px !important; }
    .test-card { background-color: #8BC34A; border-radius: 20px; padding: 15px; margin-bottom: 10px; color: #102A43; }
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; z-index: 1000; border-top: 1px solid #ccc; }
    </style>
    """, unsafe_allow_html=True)

# 2. DİNAMİK VERİ YAPISI (Dersler ve Testler)
DERS_VERILERI = {
    "Matematik": [
        {"id": "mat1", "ad": "Doğal Sayılar Test 1", "sorular": [
            {"s": "25 + 34 işleminin sonucu kaçtır?", "a": "54", "b": "59", "c": "60", "d": "61", "cvp": "B"}
        ]},
        {"id": "mat2", "ad": "Çarpma İşlemi Test 1", "sorular": []}
    ],
    "Fen Bilimleri": [
        {"id": "fen1", "ad": "Güneş'in Yapısı Test 1", "sorular": [
            {"s": "Güneş ne tür bir gök cismidir?", "a": "Gezegen", "b": "Uydu", "c": "Yıldız", "d": "Bulutsu", "cvp": "C"}
        ]},
        {"id": "fen2", "ad": "Ay'ın Evreleri Test 1", "sorular": []}
    ],
    "Türkçe": [
        {"id": "tur1", "ad": "Sözcükte Anlam Test 1", "sorular": []}
    ]
}

# 3. OTURUM YÖNETİMİ (Session State)
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'secilen_ders' not in st.session_state: st.session_state.secilen_ders = None
if 'secilen_test_id' not in st.session_state: st.session_state.secilen_test_id = None
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0

# GERÇEK VERİLER: Her testin sonucunu burada saklıyoruz (Başlangıçta hepsi 0)
if 'istatistikler' not in st.session_state:
    st.session_state.istatistikler = {tid: {"d": 0, "y": 0, "p": 0} for ders in DERS_VERILERI.values() for tid in [t["id"] for t in ders]}

def navigate(to):
    st.session_state.page = to
    st.rerun()

# 4. SAYFALAR

# --- ANA SAYFA ---
if st.session_state.page == 'home':
    st.markdown('<h2 style="color:white; text-align:center;">5. Sınıf Tüm Dersler</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝\nTestler"): navigate('kategoriler')
        if st.button("🎬\nVideolar"): pass
    with col2:
        if st.button("❓\nRastgele"): pass
        if st.button("❤️\nFavoriler"): pass
    with col3:
        if st.button("📖\nKonu"): pass
        if st.button("📊\nİstatistik"): pass
    st.button("🚫 Reklamları Kaldır", use_container_width=True)

# --- KATEGORİLER (DERS SEÇİMİ) ---
elif st.session_state.page == 'kategoriler':
    st.markdown('<h3 style="color:white; border-bottom: 1px solid #444;">KATEGORİLER</h3>', unsafe_allow_html=True)
    for ders_adi in DERS_VERILERI.keys():
        st.markdown('<div class="cat-card">', unsafe_allow_html=True)
        if st.button(f"📚 {ders_adi} \n ✓ Kategori"):
            st.session_state.secilen_ders = ders_adi
            navigate('test_listesi')
        st.markdown('</div>', unsafe_allow_html=True)
    if st.button("⬅️ Geri"): navigate('home')

# --- TEST LİSTESİ (DERSE ÖZEL VE GERÇEK VERİLİ) ---
elif st.session_state.page == 'test_listesi':
    ders = st.session_state.secilen_ders
    st.markdown(f'<h3 style="color:white;">{ders} Testleri</h3>', unsafe_allow_html=True)
    
    for test in DERS_VERILERI[ders]:
        stats = st.session_state.istatistikler[test["id"]]
        soru_sayisi = len(test["sorular"])
        
        st.markdown(f"""
            <div class="test-card">
                <div style="font-weight:bold;">📋 {test['ad']}</div>
                <div style="font-size:12px;">✓ İstatistiklerim</div>
                <div style="display:flex; justify-content:space-around; background:rgba(255,255,255,0.2); border-radius:10px; padding:5px; margin-top:10px; text-align:center;">
                    <div>{soru_sayisi}<br><small>SORU</small></div>
                    <div>{stats['d']}<br><small>DOĞRU</small></div>
                    <div>{stats['y']}<br><small>YANLIŞ</small></div>
                    <div>{stats['p']}<br><small>PUAN</small></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🔄 Yeniden Çöz", key=test["id"]):
            if soru_sayisi > 0:
                st.session_state.secilen_test_id = test["id"]
                st.session_state.q_idx = 0
                navigate('quiz')
            else:
                st.warning("Bu testin soruları henüz eklenmedi.")
    
    if st.button("⬅️ Kategorilere Dön"): navigate('kategoriler')

# --- SORU EKRANI ---
elif st.session_state.page == 'quiz':
    # Seçilen testi bul
    ders_adi = st.session_state.secilen_ders
    test_id = st.session_state.secilen_test_id
    test_verisi = next(t for t in DERS_VERILERI[ders_adi] if t["id"] == test_id)
    soru = test_verisi["sorular"][st.session_state.q_idx]
    
    stats = st.session_state.istatistikler[test_id]

    st.markdown(f"""
        <div class="quiz-header">
            <span>⏰ 02:30</span>
            <span style="font-weight:bold;">{st.session_state.q_idx + 1} / {len(test_verisi['sorular'])}</span>
            <span class="score-badge wrong-bg">{stats['y']}</span>
            <span class="score-badge correct-bg">{stats['d']}</span>
            <span>📝</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    for harf in ['a', 'b', 'c', 'd']:
        if st.button(f"{harf.upper()}) {soru[harf]}", key=f"q_{harf}"):
            if harf.upper() == soru["cvp"]:
                st.session_state.istatistikler[test_id]["d"] += 1
                st.session_state.istatistikler[test_id]["p"] += 10
                st.success("DOĞRU!")
            else:
                st.session_state.istatistikler[test_id]["y"] += 1
                st.error(f"YANLIŞ! Doğru: {soru['cvp']}")
            
            # 1 saniye sonra diğer soruya veya listeye dön
            if st.session_state.q_idx < len(test_verisi['sorular']) - 1:
                st.session_state.q_idx += 1
            else:
                st.balloons()
                st.info("Test Tamamlandı!")
                if st.button("Listeye Dön"): navigate('test_listesi')

    if st.button("❌ Testten Çık"): navigate('test_listesi')

# SABİT ALT NAVİGASYON
st.markdown('<div class="nav-bar">🏠 📋 📊 ❤️ ◀️</div>', unsafe_allow_html=True)
