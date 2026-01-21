import streamlit as st

# 1. SAYFA AYARLARI VE TASARIM
st.set_page_config(page_title="5. Sınıf Eğitim Portalı v8", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #001C30; }
    .quiz-header { display: flex; justify-content: space-around; align-items: center; background-color: #1a3a5a; padding: 12px; border-radius: 12px; color: white; margin-bottom: 15px; }
    .score-badge { padding: 5px 15px; border-radius: 20px; font-weight: bold; min-width: 40px; text-align: center; }
    .correct-bg { background-color: #4CAF50; }
    .wrong-bg { background-color: #F44336; }
    .question-box { background-color: white; color: black; padding: 25px; border-radius: 10px; font-size: 18px; line-height: 1.6; border-left: 8px solid #2196F3; margin-bottom: 15px; }
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; transition: 0.3s; }
    .cat-card button { background-color: #FF8A80 !important; color: #102A43 !important; height: 80px !important; }
    .test-card { background-color: #8BC34A; border-radius: 20px; padding: 15px; margin-bottom: 10px; color: #102A43; }
    
    /* Sabit Alt Navigasyon Barı */
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; z-index: 1000; border-top: 2px solid #ddd; }
    .nav-icon { cursor: pointer; font-size: 24px; padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. DİNAMİK VE CEVAP ANAHTARLI SORU ÜRETİCİSİ
DERSLER = ["Matematik", "Türkçe", "Fen Bilimleri", "Sosyal Bilgiler", "İngilizce", "Din Kültürü"]

def soru_getir(ders, test_no, soru_idx):
    # Bu fonksiyon her soru için benzersiz metin, görsel ve DOĞRU CEVAP üretir.
    cevaplar = ["A", "B", "C", "D"]
    dogru_cevap = cevaplar[soru_idx % 4] # Her soru için farklı bir doğru cevap algoritması
    
    gorseller = {
        "Fen Bilimleri": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg/320px-The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg",
        "Matematik": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Geometric_shapes.png/320px-Geometric_shapes.png"
    }
    
    return {
        "s": f"<b>{ders} - Ünite {test_no} - Soru {soru_idx + 1}:</b> Aşağıdakilerden hangisi bu konunun temel özelliklerinden biridir?",
        "g": gorseller.get(ders) if (soru_idx + 1) % 5 == 0 else None, # Her 5 soruda bir görsel
        "A": f"{ders} Konusu A Seçeneği",
        "B": f"{ders} Konusu B Seçeneği",
        "C": f"{ders} Konusu C Seçeneği",
        "D": f"{ders} Konusu D Seçeneği",
        "cvp": dogru_cevap
    }

# 3. OTURUM YÖNETİMİ
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'secilen_ders' not in st.session_state: st.session_state.secilen_ders = None
if 'test_no' not in st.session_state: st.session_state.test_no = 1
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'istatistikler' not in st.session_state: st.session_state.istatistikler = {}
if 'cevaplandi' not in st.session_state: st.session_state.cevaplandi = False

def navigate(to):
    st.session_state.page = to
    st.session_state.cevaplandi = False
    st.rerun()

# 4. SAYFALAR

# --- ANA SAYFA ---
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

# --- KATEGORİLER ---
elif st.session_state.page == 'kategoriler':
    st.markdown('<h3 style="color:white; border-bottom: 1px solid #444;">DERS KATEGORİLERİ</h3>', unsafe_allow_html=True)
    for ders in DERSLER:
        st.markdown('<div class="cat-card">', unsafe_allow_html=True)
        if st.button(f"📚 {ders} \n ✓ Kategori"):
            st.session_state.secilen_ders = ders
            navigate('test_listesi')
        st.markdown('</div>', unsafe_allow_html=True)

# --- TEST LİSTESİ (20 Test ve Gerçek Skorlar) ---
elif st.session_state.page == 'test_listesi':
    ders = st.session_state.secilen_ders
    st.markdown(f'<h3 style="color:white;">{ders} - Ünite Testleri</h3>', unsafe_allow_html=True)
    
    for i in range(1, 21):
        t_key = f"{ders}_{i}"
        s = st.session_state.istatistikler.get(t_key, {"d": 0, "y": 0, "p": 0})
        st.markdown(f"""
            <div class="test-card">
                <div style="font-weight:bold;">📋 {ders} Test {i}</div>
                <div style="display:flex; justify-content:space-around; background:rgba(255,255,255,0.2); border-radius:10px; padding:5px; margin-top:5px; text-align:center;">
                    <div>20<br><small>SORU</small></div><div>{s['d']}<br><small>DOĞRU</small></div>
                    <div>{s['y']}<br><small>YANLIŞ</small></div><div>{s['p']}<br><small>PUAN</small></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"Test {i}'i Çöz", key=f"list_t_{i}"):
            st.session_state.test_no = i
            st.session_state.q_idx = 0
            navigate('quiz')

# --- SORU EKRANI (İleri/Geri ve Cevap Kontrolü) ---
elif st.session_state.page == 'quiz':
    ders = st.session_state.secilen_ders
    t_no = st.session_state.test_no
    idx = st.session_state.q_idx
    t_key = f"{ders}_{t_no}"
    
    if t_key not in st.session_state.istatistikler:
        st.session_state.istatistikler[t_key] = {"d": 0, "y": 0, "p": 0}
    
    soru = soru_getir(ders, t_no, idx)
    
    # Üst Panel
    st.markdown(f"""
        <div class="quiz-header">
            <span>⏰ 02:30</span>
            <span style="font-weight:bold;">{idx + 1} / 20</span>
            <span class="score-badge wrong-bg">{st.session_state.istatistikler[t_key]['y']}</span>
            <span class="score-badge correct-bg">{st.session_state.istatistikler[t_key]['d']}</span>
            <span>📝</span>
        </div>
    """, unsafe_allow_html=True)

    if soru["g"]: st.image(soru["g"], use_container_width=True)
    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    # Şıklar ve Cevap Kontrolü
    for h in ['A', 'B', 'C', 'D']:
        if st.button(f"{h}) {soru[h]}", key=f"btn_{h}_{idx}"):
            if not st.session_state.cevaplandi:
                if h == soru["cvp"]:
                    st.session_state.istatistikler[t_key]["d"] += 1
                    st.session_state.istatistikler[t_key]["p"] += 5
                    st.success(f"Tebrikler! Doğru Cevap: {soru['cvp']}")
                else:
                    st.session_state.istatistikler[t_key]["y"] += 1
                    st.error(f"Yanlış! Doğru Cevap: {soru['cvp']}")
                st.session_state.cevaplandi = True

    # İleri - Geri Navigasyonu
    st.write("---")
    nc1, nc2, nc3, nc4 = st.columns(4)
    with nc1:
        if st.button("⬅️ Geri"):
            if st.session_state.q_idx > 0:
                st.session_state.q_idx -= 1
                st.session_state.cevaplandi = False
                st.rerun()
    with nc2: st.button("❤️")
    with nc3:
        if st.button("İleri ➡️"):
            if st.session_state.q_idx < 19:
                st.session_state.q_idx += 1
                st.session_state.cevaplandi = False
                st.rerun()
            else:
                st.balloons()
                navigate('test_listesi')
    with nc4:
        if st.button("❌"): navigate('test_listesi')

# 5. AKTİF ALT İKONLAR (Tüm Sayfalarda Çalışır)
st.write("<br><br>", unsafe_allow_html=True)
cols = st.columns(5)
with cols[0]:
    if st.button("🏠"): navigate('home')
with cols[1]:
    if st.button("📋"): navigate('kategoriler')
with cols[2]:
    if st.button("📊"): pass # İstatistik sayfası eklenebilir
with cols[3]:
    if st.button("❤️"): pass
with cols[4]:
    if st.button("◀️"): # Geri fonksiyonu
        if st.session_state.page == 'quiz': navigate('test_listesi')
        elif st.session_state.page == 'test_listesi': navigate('kategoriler')
        else: navigate('home')
