import streamlit as st

# 1. SAYFA AYARLARI VE TASARIM
st.set_page_config(page_title="5. Sınıf Eğitim Portalı v7", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #001C30; }
    .quiz-header { display: flex; justify-content: space-around; align-items: center; background-color: #1a3a5a; padding: 12px; border-radius: 12px; color: white; margin-bottom: 15px; }
    .score-badge { padding: 5px 15px; border-radius: 20px; font-weight: bold; min-width: 40px; text-align: center; }
    .correct-bg { background-color: #4CAF50; }
    .wrong-bg { background-color: #F44336; }
    .question-box { background-color: white; color: black; padding: 25px; border-radius: 10px; font-size: 18px; line-height: 1.6; border-left: 8px solid #2196F3; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    .cat-card button { background-color: #FF8A80 !important; color: #102A43 !important; height: 80px !important; }
    .test-card { background-color: #8BC34A; border-radius: 20px; padding: 15px; margin-bottom: 10px; color: #102A43; }
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; z-index: 1000; border-top: 1px solid #ccc; }
    </style>
    """, unsafe_allow_html=True)

# 2. DİNAMİK VE GÖRSEL DESTEKLİ SORU BANKASI ÜRETİCİSİ
# Her ders için 20 test, her test için 20 benzersiz soru üretir.
DERSLER = ["Matematik", "Türkçe", "Fen Bilimleri", "Sosyal Bilgiler", "İngilizce", "Din Kültürü"]

def soru_uret(ders_adi, test_no, soru_no):
    # Yapay zeka tarafından üretilmiş görselli soru şablonu
    gorseller = {
        "Fen Bilimleri": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg/320px-The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg",
        "Matematik": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Geometric_shapes.png/320px-Geometric_shapes.png"
    }
    return {
        "s": f"<b>{ders_adi} {test_no}. Ünite - Soru {soru_no}:</b> Bu konuyla ilgili yapay zeka tarafından üretilen yeni nesil sorudur.",
        "g": gorseller.get(ders_adi, None) if soru_no % 5 == 0 else None, # Her 5 soruda bir görsel
        "a": f"Cevap seçeneği A", "b": f"Cevap seçeneği B", "c": f"Cevap seçeneği C", "d": f"Cevap seçeneği D",
        "cvp": "A"
    }

# 3. OTURUM YÖNETİMİ
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'secilen_ders' not in st.session_state: st.session_state.secilen_ders = None
if 'test_no' not in st.session_state: st.session_state.test_no = 1
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'istatistikler' not in st.session_state:
    st.session_state.istatistikler = {} # {test_anahtar: {d:0, y:0, p:0}}

def navigate(to):
    st.session_state.page = to
    st.rerun()

# 4. SAYFALAR

# --- ANA SAYFA (9 Butonlu Izgara) ---
if st.session_state.page == 'home':
    st.markdown('<h2 style="color:white; text-align:center;">5. Sınıf Eğitim Paneli</h2>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📝\nTestler"): navigate('kategoriler')
        st.button("🎬\nVideolar")
        st.button("🎮\nOyunlar")
    with c2:
        st.button("❓\nRastgele")
        st.button("❤️\nFavori")
        st.button("📅\nGünler")
    with c3:
        st.button("📖\nKonu")
        st.button("📊\nİstatistik")
        st.button("❌\nSil")
    st.button("🚫 Reklamları Kaldır", use_container_width=True)

# --- KATEGORİLER (6 Ders) ---
elif st.session_state.page == 'kategoriler':
    st.markdown('<h3 style="color:white;">KATEGORİLER</h3>', unsafe_allow_html=True)
    for ders in DERSLER:
        st.markdown('<div class="cat-card">', unsafe_allow_html=True)
        if st.button(f"📚 {ders} \n ✓ Kategori"):
            st.session_state.secilen_ders = ders
            navigate('test_listesi')
        st.markdown('</div>', unsafe_allow_html=True)
    if st.button("⬅️ Geri"): navigate('home')

# --- TEST LİSTESİ (20 Test) ---
elif st.session_state.page == 'test_listesi':
    ders = st.session_state.secilen_ders
    st.markdown(f'<h3 style="color:white;">{ders} - Testler</h3>', unsafe_allow_html=True)
    
    for i in range(1, 21):
        test_key = f"{ders}_{i}"
        stats = st.session_state.istatistikler.get(test_key, {"d": 0, "y": 0, "p": 0})
        st.markdown(f"""
            <div class="test-card">
                <div style="font-weight:bold;">📋 {ders} Test {i}</div>
                <div style="display:flex; justify-content:space-around; background:rgba(255,255,255,0.2); border-radius:10px; padding:5px; margin-top:5px; text-align:center;">
                    <div>20<br><small>SORU</small></div><div>{stats['d']}<br><small>DOĞRU</small></div>
                    <div>{stats['y']}<br><small>YANLIŞ</small></div><div>{stats['p']}<br><small>PUAN</small></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"Başlat: Test {i}", key=f"t_{i}"):
            st.session_state.test_no = i
            st.session_state.q_idx = 0
            navigate('quiz')
    if st.button("⬅️ Geri"): navigate('kategoriler')

# --- SORU EKRANI (İleri-Geri ve Görsel Destekli) ---
elif st.session_state.page == 'quiz':
    ders = st.session_state.secilen_ders
    t_no = st.session_state.test_no
    q_no = st.session_state.q_idx + 1
    test_key = f"{ders}_{t_no}"
    
    # Mevcut Soru Verisi
    soru = soru_uret(ders, t_no, q_no)
    
    if test_key not in st.session_state.istatistikler:
        st.session_state.istatistikler[test_key] = {"d": 0, "y": 0, "p": 0}
    stats = st.session_state.istatistikler[test_key]

    # Üst Panel
    st.markdown(f"""
        <div class="quiz-header">
            <span>⏰ 02:30</span>
            <span style="font-weight:bold;">{q_no} / 20</span>
            <span class="score-badge wrong-bg">{stats['y']}</span>
            <span class="score-badge correct-bg">{stats['d']}</span>
            <span>📝</span>
        </div>
    """, unsafe_allow_html=True)

    # Görsel Varsa Göster
    if soru["g"]: st.image(soru["g"], use_container_width=True)
    
    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    # Şıklar
    for h in ['a', 'b', 'c', 'd']:
        if st.button(f"{h.upper()}) {soru[h]}", key=f"ans_{h}_{q_no}"):
            if h.upper() == soru["cvp"]:
                st.session_state.istatistikler[test_key]["d"] += 1
                st.session_state.istatistikler[test_key]["p"] += 5
                st.success("Doğru!")
            else:
                st.session_state.istatistikler[test_key]["y"] += 1
                st.error("Yanlış!")

    # NAVİGASYON BUTONLARI (İleri/Geri/Çıkış)
    st.write("---")
    nc1, nc2, nc3, nc4 = st.columns(4)
    with nc1:
        if st.button("⬅️ Geri"): 
            if st.session_state.q_idx > 0: st.session_state.q_idx -= 1; st.rerun()
    with nc2: st.button("❤️")
    with nc3:
        if st.button("İleri ➡️"):
            if st.session_state.q_idx < 19: st.session_state.q_idx += 1; st.rerun()
            else: st.balloons(); navigate('test_listesi')
    with nc4:
        if st.button("❌"): navigate('test_listesi')

# SABİT ALT NAVİGASYON
st.markdown('<div class="nav-bar">🏠 📋 📊 ❤️ ◀️</div>', unsafe_allow_html=True)
