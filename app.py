import streamlit as st

# 1. SAYFA AYARLARI VE TASARIM (CSS)
st.set_page_config(page_title="5. Sınıf Eğitim Portalı", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #001C30; }
    .quiz-header { display: flex; justify-content: space-around; align-items: center; background-color: #1a3a5a; padding: 12px; border-radius: 12px; color: white; margin-bottom: 15px; }
    .score-badge { padding: 5px 15px; border-radius: 20px; font-weight: bold; min-width: 40px; text-align: center; }
    .correct-bg { background-color: #4CAF50; }
    .wrong-bg { background-color: #F44336; }
    .question-box { background-color: white; color: black; padding: 25px; border-radius: 10px; font-size: 18px; line-height: 1.6; border-left: 8px solid #2196F3; }
    .stButton>button { width: 100%; border-radius: 12px; height: 55px; font-weight: bold; }
    .cat-card button { background-color: #FF8A80 !important; color: #102A43 !important; height: 80px !important; }
    .test-card { background-color: #8BC34A; border-radius: 20px; padding: 15px; margin-bottom: 10px; color: #102A43; }
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; z-index: 1000; border-top: 1px solid #ccc; }
    </style>
    """, unsafe_allow_html=True)

# 2. DEV SORU BANKASI YAPISI (20 TEST x 20 SORU ŞABLONU)
# Örnek olarak ilk üniteleri doldurdum, yapı tüm dersler için hazırlandı.
DERS_VERILERI = {
    "Matematik": [{"id": f"mat_{i}", "ad": f"Matematik Test {i}", "sorular": [{"s": f"Matematik Soru {j}: 5. Sınıf müfredat sorusu...", "a": "Şık A", "b": "Şık B", "c": "Şık C", "d": "Şık D", "cvp": "A"} for j in range(1, 21)]} for i in range(1, 21)],
    "Türkçe": [{"id": f"tur_{i}", "ad": f"Türkçe Test {i}", "sorular": [{"s": f"Türkçe Soru {j}: Paragrafta anlam...", "a": "A", "b": "B", "c": "C", "d": "D", "cvp": "B"} for j in range(1, 21)]} for i in range(1, 21)],
    "Fen Bilimleri": [{"id": f"fen_{i}", "ad": f"Fen Bilimleri Test {i}", "sorular": [{"s": f"Fen Soru {j}: Güneş ve Ay...", "a": "A", "b": "B", "c": "C", "d": "D", "cvp": "C"} for j in range(1, 21)]} for i in range(1, 21)],
    "Sosyal Bilgiler": [{"id": f"sos_{i}", "ad": f"Sosyal Bilgiler Test {i}", "sorular": [{"s": f"Sosyal Soru {j}: Haklarımızı öğreniyoruz...", "a": "A", "b": "B", "c": "C", "d": "D", "cvp": "D"} for j in range(1, 21)]} for i in range(1, 21)],
    "İngilizce": [{"id": f"ing_{i}", "ad": f"İngilizce Test {i}", "sorular": [{"s": f"English Question {j}: Hello!...", "a": "Hi", "b": "Bye", "c": "No", "d": "Yes", "cvp": "A"} for j in range(1, 21)]} for i in range(1, 21)],
    "Din Kültürü": [{"id": f"din_{i}", "ad": f"Din Kültürü Test {i}", "sorular": [{"s": f"Din Soru {j}: Güzel ahlak...", "a": "A", "b": "B", "c": "C", "d": "D", "cvp": "B"} for j in range(1, 21)]} for i in range(1, 21)]
}

# 3. OTURUM YÖNETİMİ
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'secilen_ders' not in st.session_state: st.session_state.secilen_ders = None
if 'secilen_test_id' not in st.session_state: st.session_state.secilen_test_id = None
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'istatistikler' not in st.session_state:
    st.session_state.istatistikler = {t["id"]: {"d": 0, "y": 0, "p": 0} for ders in DERS_VERILERI.values() for t in ders}

def navigate(to):
    st.session_state.page = to
    st.rerun()

# 4. SAYFALAR

# --- ANA SAYFA (3x3 Grid) ---
if st.session_state.page == 'home':
    st.markdown('<h2 style="color:white; text-align:center;">5. Sınıf Tüm Dersler</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝\nTestler"): navigate('kategoriler')
        if st.button("🎬\nVideolar"): pass
        if st.button("🎮\nOyunlar"): pass
    with col2:
        if st.button("❓\nRastgele"): pass
        if st.button("❤️\nFavori"): pass
        if st.button("📅\nGünler"): pass
    with col3:
        if st.button("📖\nKonu"): pass
        if st.button("📊\nİstatistik"): pass
        if st.button("❌\nSil"): pass
    st.button("🚫 Reklamları Kaldır", use_container_width=True)

# --- KATEGORİLER (6 Ders Tam Liste) ---
elif st.session_state.page == 'kategoriler':
    st.markdown('<h3 style="color:white; border-bottom: 1px solid #444;">KATEGORİLER</h3>', unsafe_allow_html=True)
    for ders_adi in DERS_VERILERI.keys():
        st.markdown('<div class="cat-card">', unsafe_allow_html=True)
        if st.button(f"📚 {ders_adi} \n ✓ Kategori"):
            st.session_state.secilen_ders = ders_adi
            navigate('test_listesi')
        st.markdown('</div>', unsafe_allow_html=True)
    if st.button("⬅️ Geri"): navigate('home')

# --- TEST LİSTESİ (Gerçek Verili) ---
elif st.session_state.page == 'test_listesi':
    ders = st.session_state.secilen_ders
    st.markdown(f'<h3 style="color:white;">{ders} Üniteleri</h3>', unsafe_allow_html=True)
    
    for test in DERS_VERILERI[ders]:
        stats = st.session_state.istatistikler[test["id"]]
        st.markdown(f"""
            <div class="test-card">
                <div style="font-weight:bold;">📋 {test['ad']}</div>
                <div style="display:flex; justify-content:space-around; background:rgba(255,255,255,0.2); border-radius:10px; padding:5px; margin-top:5px; text-align:center;">
                    <div>{len(test['sorular'])}<br><small>SORU</small></div>
                    <div>{stats['d']}<br><small>DOĞRU</small></div>
                    <div>{stats['y']}<br><small>YANLIŞ</small></div>
                    <div>{stats['p']}<br><small>PUAN</small></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"Çöz: {test['ad']}", key=test["id"]):
            st.session_state.secilen_test_id = test["id"]
            st.session_state.q_idx = 0
            navigate('quiz')
    if st.button("⬅️ Geri"): navigate('kategoriler')

# --- SORU ÇÖZME EKRANI (20 Soru Döngüsü) ---
elif st.session_state.page == 'quiz':
    test_id = st.session_state.secilen_test_id
    ders_adi = st.session_state.secilen_ders
    test_verisi = next(t for t in DERS_VERILERI[ders_adi] if t["id"] == test_id)
    soru = test_verisi["sorular"][st.session_state.q_idx]
    stats = st.session_state.istatistikler[test_id]

    st.markdown(f"""
        <div class="quiz-header">
            <span>⏰ 02:30</span>
            <span style="font-weight:bold;">{st.session_state.q_idx + 1} / 20</span>
            <span class="score-badge wrong-bg">{stats['y']}</span>
            <span class="score-badge correct-bg">{stats['d']}</span>
            <span>📝</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    for h in ['a', 'b', 'c', 'd']:
        if st.button(f"{h.upper()}) {soru[h]}", key=f"ans_{h}"):
            if h.upper() == soru["cvp"]:
                st.session_state.istatistikler[test_id]["d"] += 1
                st.session_state.istatistikler[test_id]["p"] += 5
                st.success("DOĞRU!")
            else:
                st.session_state.istatistikler[test_id]["y"] += 1
                st.error(f"YANLIŞ! Cevap: {soru['cvp']}")
            
            if st.session_state.q_idx < 19:
                st.session_state.q_idx += 1
                st.rerun()
            else:
                st.balloons()
                st.success("Testi Tamamladın!")
                if st.button("Sonuçlara Git"): navigate('test_listesi')

    if st.button("🛑 Testi Yarıda Kes"): navigate('test_listesi')

# SABİT ALT NAVİGASYON
st.markdown('<div class="nav-bar">🏠 📋 📊 ❤️ ◀️</div>', unsafe_allow_html=True)
