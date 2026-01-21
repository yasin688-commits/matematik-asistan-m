import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Akıllı Test Paneli v5", layout="centered")

# --- GELİŞMİŞ CSS ---
st.markdown("""
    <style>
    .main { background-color: #001C30; }
    .quiz-header {
        display: flex; justify-content: space-around; align-items: center;
        background-color: #1a3a5a; padding: 15px; border-radius: 12px; color: white; margin-bottom: 15px;
    }
    .score-badge { padding: 5px 15px; border-radius: 20px; font-weight: bold; min-width: 40px; text-align: center; }
    .correct-bg { background-color: #4CAF50; }
    .wrong-bg { background-color: #F44336; }
    .question-box {
        background-color: white; color: black; padding: 25px; border-radius: 10px;
        font-size: 18px; line-height: 1.6; margin-bottom: 10px; border-left: 8px solid #2196F3;
    }
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; z-index: 100; }
    .stButton>button { border-radius: 12px; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SORU BANKASI (Yapay Zeka Destekli Şablon) ---
# Burada her ders için görselleştirilebilir, kaliteli sorular bulunur.
SORU_BANKASI = [
    {
        "id": 1,
        "soru": "Güneş ile ilgili verilen bilgilerden hangisi <b>yanlıştır</b>?",
        "gorsel": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg/320px-The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg",
        "A": "Isı ve ışık kaynağımızdır.",
        "B": "Dünya'nın etrafında dolanır.",
        "C": "Küre şeklindedir.",
        "D": "Sıcak gazlardan oluşur.",
        "cevap": "B"
    },
    {
        "id": 2,
        "soru": "Ay'ın evreleri ile ilgili görseldeki 'karanlık' evrenin adı nedir?",
        "gorsel": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Lunar_libration_with_phase2.gif/280px-Lunar_libration_with_phase2.gif",
        "A": "Dolunay",
        "B": "İlk Dördün",
        "C": "Yeni Ay",
        "D": "Son Dördün",
        "cevap": "C"
    },
    {
        "id": 3,
        "soru": "Dünya, Güneş ve Ay'ın büyüklük sıralaması nasıldır?",
        "gorsel": None,
        "A": "Güneş > Dünya > Ay",
        "B": "Ay > Dünya > Güneş",
        "C": "Dünya > Ay > Güneş",
        "D": "Güneş > Ay > Dünya",
        "cevap": "A"
    }
]

# --- OTURUM YÖNETİMİ ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0 # 0'dan başlar
if 'score_d' not in st.session_state: st.session_state.score_d = 0
if 'score_y' not in st.session_state: st.session_state.score_y = 0
if 'selected' not in st.session_state: st.session_state.selected = None

def change_page(target):
    st.session_state.page = target
    st.rerun()

# --- SAYFALAR ---

if st.session_state.page == 'home':
    st.markdown('<h2 style="color:white; text-align:center;">5. Sınıf Tüm Dersler</h2>', unsafe_allow_html=True)
    if st.button("📝 Testlere Başla", use_container_width=True): change_page('quiz')

elif st.session_state.page == 'quiz':
    current_q = SORU_BANKASI[st.session_state.q_idx]

    # Üst Bilgi Barı
    st.markdown(f"""
        <div class="quiz-header">
            <span>⏰ 02:30</span>
            <span style="font-weight:bold;">{st.session_state.q_idx + 1} / {len(SORU_BANKASI)}</span>
            <span class="score-badge wrong-bg">{st.session_state.score_y}</span>
            <span class="score-badge correct-bg">{st.session_state.score_d}</span>
            <span>📝</span>
        </div>
    """, unsafe_allow_html=True)

    # Görsel Varsa Göster [Görselli soru desteği]
    if current_q["gorsel"]:
        st.image(current_q["gorsel"], use_container_width=True)

    # Soru Alanı
    st.markdown(f'<div class="question-box">{current_q["soru"]}</div>', unsafe_allow_html=True)

    # Şıklar - Şık metinleri artık butonların altında/yanında net görünüyor
    colA, colB = st.columns(2)
    colC, colD = st.columns(2)

    with colA:
        if st.button(f"A) {current_q['A']}", key="A"): st.session_state.selected = "A"
    with colB:
        if st.button(f"B) {current_q['B']}", key="B"): st.session_state.selected = "B"
    with colC:
        if st.button(f"C) {current_q['C']}", key="C"): st.session_state.selected = "C"
    with colD:
        if st.button(f"D) {current_q['D']}", key="D"): st.session_state.selected = "D"

    if st.session_state.selected:
        if st.session_state.selected == current_q["cevap"]:
            st.success(f"Tebrikler! Doğru Cevap: {current_q['cevap']}")
        else:
            st.error(f"Yanlış! Doğru Cevap: {current_q['cevap']}")

    # Alt Navigasyon - Soruyu Değiştiren Kısım
    st.write("---")
    f_col = st.columns([1,1,1,1])
    with f_col[0]: st.button("⚠️")
    with f_col[1]: st.button("❤️")
    with f_col[2]: 
        if st.button("➡️ Sonraki"):
            if st.session_state.selected == current_q["cevap"]: st.session_state.score_d += 1
            else: st.session_state.score_y += 1
            
            if st.session_state.q_idx < len(SORU_BANKASI) - 1:
                st.session_state.q_idx += 1
                st.session_state.selected = None
                st.rerun()
            else:
                st.balloons()
                st.success("Test Tamamlandı!")
                if st.button("Başa Dön"): 
                    st.session_state.q_idx = 0
                    change_page('home')
    with f_col[3]:
        if st.button("❌"): change_page('home')

# SABİT ALT NAVİGASYON
st.markdown('<div class="nav-bar">🏠 📋 📊 ❤️ ◀️</div>', unsafe_allow_html=True)
