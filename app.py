import streamlit as st

# 1. SAYFA AYARLARI VE TASARIM (CSS)
st.set_page_config(page_title="5. Sınıf Eğitim Paneli", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #001C30; }
    
    /* Üst Bar Tasarımı */
    .quiz-header {
        display: flex; justify-content: space-around; align-items: center;
        background-color: #1a3a5a; padding: 12px; border-radius: 12px; color: white; margin-bottom: 15px;
    }
    .score-badge { padding: 5px 15px; border-radius: 20px; font-weight: bold; min-width: 40px; text-align: center; }
    .correct-bg { background-color: #4CAF50; }
    .wrong-bg { background-color: #F44336; }
    
    /* Soru Kutusu */
    .question-box {
        background-color: white; color: black; padding: 25px; border-radius: 10px;
        font-size: 18px; line-height: 1.6; margin-bottom: 15px; border-left: 8px solid #2196F3;
    }
    
    /* Ana Sayfa Butonları */
    .stButton>button { width: 100%; border-radius: 12px; height: 60px; font-weight: bold; }
    
    /* Kategori Kartları (Somon Rengi) */
    .cat-card button { background-color: #FF8A80 !important; color: #102A43 !important; height: 80px !important; }

    /* Test Listesi Kartları (Yeşil) */
    .test-card { background-color: #8BC34A; border-radius: 20px; padding: 15px; margin-bottom: 10px; color: #102A43; }

    /* Sabit Alt Navigasyon */
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; z-index: 1000; border-top: 1px solid #ccc; }
    </style>
    """, unsafe_allow_html=True)

# 2. YAPAY ZEKA DESTEKLİ SORU BANKASI
SORU_BANKASI = [
    {
        "id": 1,
        "soru": "<b>Soru 1:</b> Güneş ile ilgili bilgi edinmek için bazı yöntemlerden yararlanılır. Aşağıdakilerden hangisi Güneş ile ilgili bilgi edinmek için doğru bir yöntem <u>değildir</u>?",
        "gorsel": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg/320px-The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg",
        "A": "Uzaydaki teleskopların çektiği fotoğrafları incelemek",
        "B": "Güneş'in mevsimlere göre konumunu karşılaştırmak",
        "C": "Büyüteç ve merceklerle Güneş'e doğrudan bakmak",
        "D": "Güneş'e yakın uçuş yapacak uzay araçları tasarlamak",
        "cevap": "C"
    },
    {
        "id": 2,
        "soru": "<b>Soru 2:</b> Ay'ın kendi ekseni etrafındaki dönüş süresi ile Dünya etrafındaki dolanma süresi eşit olduğu için hangisi gerçekleşir?",
        "gorsel": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/280px-FullMoon2010.jpg",
        "A": "Ay her zaman dolunay görünür.",
        "B": "Ay'ın hep aynı yüzünü görürüz.",
        "C": "Ay'ın evreleri oluşmaz.",
        "D": "Dünya, Ay'dan daha hızlı döner.",
        "cevap": "B"
    }
]

# 3. OTURUM YÖNETİMİ (SESSION STATE)
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'corrects' not in st.session_state: st.session_state.corrects = 0
if 'wrongs' not in st.session_state: st.session_state.wrongs = 0
if 'selected' not in st.session_state: st.session_state.selected = None

def navigate(to):
    st.session_state.page = to
    st.rerun()

# 4. SAYFA İÇERİKLERİ

# --- EKRAN 1: ANA SAYFA ---
if st.session_state.page == 'home':
    st.markdown('<h2 style="color:white; text-align:center;">4. Sınıf Testleri</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝\nTestler"): navigate('kategoriler')
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
    st.button("🚫 Reklamları Kaldır", use_container_width=True)

# --- EKRAN 2: KATEGORİLER ---
elif st.session_state.page == 'kategoriler':
    st.markdown('<h3 style="color:white; border-bottom: 1px solid #444;">KATEGORİLER</h3>', unsafe_allow_html=True)
    dersler = [("📐", "Matematik"), ("📚", "Türkçe"), ("🧪", "Fen Bilimleri"), ("🌍", "Sosyal Bilgiler"), ("🇬🇧", "İngilizce"), ("🕌", "Din Kültürü")]
    for icon, ders in dersler:
        st.markdown('<div class="cat-card">', unsafe_allow_html=True)
        if st.button(f"{icon} {ders} \n ✓ Kategori"): navigate('test_listesi')
        st.markdown('</div>', unsafe_allow_html=True)
    if st.button("⬅️ Ana Sayfaya Dön"): navigate('home')

# --- EKRAN 3: TEST LİSTESİ ---
elif st.session_state.page == 'test_listesi':
    st.markdown('<h3 style="color:white;">Güneş, Dünya ve Ay</h3>', unsafe_allow_html=True)
    tests = [("Güneş'in Yapısı Test 1", 14, 12, 2, 85), ("Ay'ın Evreleri Test 1", 12, 10, 2, 80)]
    for title, q, d, y, p in tests:
        st.markdown(f"""
            <div class="test-card">
                <div style="font-weight:bold;">📋 {title}</div>
                <div style="font-size:12px;">✓ İstatistiklerim</div>
                <div style="display:flex; justify-content:space-around; background:rgba(255,255,255,0.2); border-radius:10px; padding:5px; margin-top:10px; text-align:center;">
                    <div>{q}<br><small>SORU</small></div><div>{d}<br><small>DOĞRU</small></div>
                    <div>{y}<br><small>YANLIŞ</small></div><div>{p}<br><small>PUAN</small></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"🔄 Yeniden Çöz - {title}"):
            st.session_state.q_idx = 0
            navigate('quiz')
    if st.button("⬅️ Geri Dön"): navigate('kategoriler')

# --- EKRAN 4: SORU ÇÖZME EKRANI ---
elif st.session_state.page == 'quiz':
    curr = SORU_BANKASI[st.session_state.q_idx]
    
    # Üst Bilgi Barı
    st.markdown(f"""
        <div class="quiz-header">
            <span>⏰ 02:31</span>
            <span style="font-weight:bold;">{st.session_state.q_idx + 1} / {len(SORU_BANKASI)}</span>
            <span class="score-badge wrong-bg">{st.session_state.wrongs}</span>
            <span class="score-badge correct-bg">{st.session_state.corrects}</span>
            <span>📝</span>
        </div>
    """, unsafe_allow_html=True)

    if curr["gorsel"]: st.image(curr["gorsel"], use_container_width=True)
    st.markdown(f'<div class="question-box">{curr["soru"]}</div>', unsafe_allow_html=True)

    # Şıklar (A, B, C, D)
    for key in ['A', 'B', 'C', 'D']:
        if st.button(f"{key}) {curr[key]}", key=f"btn_{key}", use_container_width=True):
            st.session_state.selected = key

    if st.session_state.selected:
        if st.session_state.selected == curr["cevap"]: st.success("Doğru!")
        else: st.error(f"Yanlış! Doğru Cevap: {curr['cevap']}")

    # Alt Fonksiyonel Butonlar
    st.write("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("⚠️")
    with c2: st.button("❤️")
    with c3:
        if st.button("➡️"): # Sonraki Soruya Geçiş Mantığı
            if st.session_state.selected:
                if st.session_state.selected == curr["cevap"]: st.session_state.corrects += 1
                else: st.session_state.wrongs += 1
                
                if st.session_state.q_idx < len(SORU_BANKASI) - 1:
                    st.session_state.q_idx += 1
                    st.session_state.selected = None
                    st.rerun()
                else:
                    st.success("Test Bitti!")
                    if st.button("Sonuçlara Dön"): navigate('test_listesi')
            else: st.warning("Lütfen bir şık seçin!")
    with c4:
        if st.button("❌"): navigate('test_listesi')

# 5. SABİT ALT NAVİGASYON (Tüm sayfalarda görünür)
st.markdown("""
    <div class="nav-bar">
        <span style="font-size:24px;">🏠</span>
        <span style="font-size:24px;">📋</span>
        <span style="font-size:24px;">📊</span>
        <span style="font-size:24px;">❤️</span>
        <span style="font-size:24px;">◀️</span>
    </div>
    """, unsafe_allow_html=True)
