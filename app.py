import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="5. Sınıf Eğitim Paneli", layout="centered")

# --- TÜM GÖRSEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #001C30; }
    
    /* Ana Sayfa Grid Kartları */
    .stButton>button { width: 100%; border-radius: 15px; font-weight: bold; }
    
    /* Kategori Kartları (Somon/Kırmızı) */
    .cat-btn button { background-color: #FF8A80 !important; color: #102A43 !important; height: 80px !important; font-size: 18px !important; }

    /* Test Listesi Kartları (Yeşil) */
    .test-card { background-color: #8BC34A; border-radius: 20px; padding: 15px; margin-bottom: 10px; color: #102A43; }
    .stats-container { display: flex; justify-content: space-around; background: rgba(255,255,255,0.2); border-radius: 10px; padding: 5px; margin-top: 10px; }
    
    /* Soru Ekranı Stili */
    .question-box { background-color: white; padding: 20px; border-radius: 15px; color: black; margin-bottom: 20px; font-size: 18px; font-weight: bold; border-left: 5px solid #2196F3; }
    
    .header-text { color: white; text-align: center; font-size: 22px; font-weight: bold; padding: 10px; border-bottom: 1px solid #444; margin-bottom: 20px; }
    
    /* Alt Navigasyon */
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; border-top: 1px solid #ccc; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

# --- OTURUM VE SAYFA YÖNETİMİ ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

def change_page(target):
    st.session_state.page = target
    st.rerun()

# --- SAYFA İÇERİKLERİ ---

# 1. ADIM: ANA SAYFA
if st.session_state.page == 'home':
    st.markdown('<p class="header-text">4. Sınıf Testleri</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝\nTestler"): change_page('kategoriler')
        if st.button("🎬\nVideolar"): pass
        if st.button("🎮\nOyunlar"): pass
    with col2:
        if st.button("❓\nRastgele"): pass
        if st.button("❤️\nFavoriler"): pass
        if st.button("📅\nTakvim"): pass
    with col3:
        if st.button("📖\nKonu"): pass
        if st.button("📊\nİstatistik"): pass
        if st.button("❌\nHesap Sil"): pass
    
    st.markdown('<div style="background-color:#689F38; color:white; padding:10px; border-radius:15px; text-align:center; margin-top:20px;">🚫 Reklamları Kaldır</div>', unsafe_allow_html=True)

# 2. ADIM: KATEGORİLER
elif st.session_state.page == 'kategoriler':
    st.markdown('<p class="header-text">KATEGORİLER</p>', unsafe_allow_html=True)
    dersler = [("📐", "Matematik"), ("📚", "Türkçe"), ("🧪", "Fen Bilimleri"), ("🌍", "Sosyal Bilgiler")]
    
    for icon, ders in dersler:
        st.markdown('<div class="cat-btn">', unsafe_allow_html=True)
        if st.button(f"{icon} {ders} \n ✓ Kategori", key=ders):
            change_page('test_listesi')
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("⬅️ Geri"): change_page('home')

# 3. ADIM: TEST LİSTESİ
elif st.session_state.page == 'test_listesi':
    st.markdown('<p class="header-text">Fen Bilimleri: Güneş ve Ay</p>', unsafe_allow_html=True)
    
    tests = [("Güneş'in Yapısı Test 1", 14, 12, 2, 85), ("Ay'ın Evreleri Test 1", 12, 10, 2, 80)]
    
    for title, q, d, y, p in tests:
        st.markdown(f"""
            <div class="test-card">
                <div style="font-weight:bold;">📋 {title}</div>
                <div class="stats-container">
                    <div>{q}<br><small>SORU</small></div>
                    <div>{d}<br><small>DOĞRU</small></div>
                    <div>{y}<br><small>YANLIŞ</small></div>
                    <div>{p}<br><small>PUAN</small></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"🔄 {title} Çöz", key=title):
            st.session_state.current_question = 0
            change_page('quiz')
            
    if st.button("⬅️ Geri"): change_page('kategoriler')

# 4. ADIM: SORU ÇÖZME EKRANI (YENİ!)
elif st.session_state.page == 'quiz':
    st.markdown('<p class="header-text">Soru 1 / 10</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="question-box">Aşağıdakilerden hangisi Güneş\'in özelliklerinden biri değildir?</div>', unsafe_allow_html=True)
    
    secenekler = ["A) Isı ve ışık kaynağıdır.", "B) Katmanlardan oluşur.", "C) Dünya'nın etrafında döner.", "D) Küre şeklindedir."]
    
    for secenek in secenekler:
        if st.button(secenek, use_container_width=True):
            st.success("Cevabınız kaydedildi!")
            # Burada bir sonraki soruya geçiş mantığı kurulabilir
    
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⬅️ Önceki"): pass
    with col_next:
        if st.button("Sonraki ➡️"): pass

    if st.button("🛑 Testi Bitir"): change_page('test_listesi')

# --- SABİT ALT NAVİGASYON ---
st.markdown("""
    <div class="nav-bar">
        <span>🏠</span><span>📋</span><span>📊</span><span>❤️</span><span>◀️</span>
    </div>
    """, unsafe_allow_html=True)
