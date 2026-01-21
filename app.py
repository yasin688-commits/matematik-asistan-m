import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Eğitim Uygulaması v4", layout="centered")

# --- TÜM GÖRSEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #001C30; }
    .quiz-header {
        display: flex; justify-content: space-around; align-items: center;
        background-color: #1a3a5a; padding: 10px; border-radius: 10px; color: white; margin-bottom: 10px;
    }
    .score-badge { padding: 5px 15px; border-radius: 15px; font-weight: bold; }
    .correct-bg { background-color: #4CAF50; }
    .wrong-bg { background-color: #F44336; }
    .question-container {
        background-color: white; color: black; padding: 20px; border-radius: 5px;
        line-height: 1.5; margin-bottom: 20px; border-bottom: 4px solid #ddd;
    }
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; border-top: 1px solid #ccc; z-index: 100; }
    /* Seçilen şıkkı vurgulamak için */
    div[data-testid="stHorizontalBlock"] button:active { background-color: #2196F3 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- OTURUM YÖNETİMİ (Session State) ---
# Uygulamanın seçimleri hatırlaması için bu kısım kritik
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'q_index' not in st.session_state: st.session_state.q_index = 1
if 'corrects' not in st.session_state: st.session_state.corrects = 4
if 'wrongs' not in st.session_state: st.session_state.wrongs = 10
if 'selected_answer' not in st.session_state: st.session_state.selected_answer = None

def change_page(target):
    st.session_state.page = target
    st.rerun()

def next_question():
    st.session_state.q_index += 1
    st.session_state.selected_answer = None # Yeni soru için seçimi sıfırla
    st.rerun()

# --- SAYFA İÇERİKLERİ ---

# ANA SAYFA (ADIM 1)
if st.session_state.page == 'home':
    st.markdown('<h3 style="color:white; text-align:center;">4. Sınıf Testleri</h3>', unsafe_allow_html=True)
    if st.button("📝 Testler", use_container_width=True): change_page('kategoriler')
    st.button("🚫 Reklamları Kaldır", use_container_width=True)

# KATEGORİLER (ADIM 2)
elif st.session_state.page == 'kategoriler':
    st.markdown('<h3 style="color:white;">KATEGORİLER</h3>', unsafe_allow_html=True)
    if st.button("🧪 Fen Bilimleri", use_container_width=True): change_page('test_listesi')
    if st.button("⬅️ Geri"): change_page('home')

# TEST LİSTESİ (ADIM 3)
elif st.session_state.page == 'test_listesi':
    st.markdown('<h3 style="color:white;">Güneş, Dünya ve Ay</h3>', unsafe_allow_html=True)
    st.markdown('<div style="background-color:#8BC34A; padding:15px; border-radius:20px; color:#102A43;"><b>📋 Güneş\'in Yapısı Test 1</b></div>', unsafe_allow_html=True)
    if st.button("🔄 Yeniden Çöz", use_container_width=True): change_page('quiz')
    if st.button("⬅️ Geri"): change_page('kategoriler')

# SORU ÇÖZME EKRANI (ADIM 4 - AKTİF ŞIKLAR VE GEÇİŞ)
elif st.session_state.page == 'quiz':
    # Üst Bilgi Barı
    st.markdown(f"""
        <div class="quiz-header">
            <span>⏰ 02:31</span>
            <span style="font-weight:bold;">{st.session_state.q_index} / 14</span>
            <span class="score-badge wrong-bg">{st.session_state.wrongs}</span>
            <span class="score-badge correct-bg">{st.session_state.corrects}</span>
            <span>📝</span>
        </div>
    """, unsafe_allow_html=True)

    # Soru Alanı
    st.markdown(f"""
        <div class="question-container">
            <b>Soru {st.session_state.q_index}:</b><br>
            Güneş ile ilgili bilgi edinmek için bazı yöntemlerden yararlanılır.<br><br>
            <b>Aşağıdakilerden hangisi Güneş ile ilgili bilgi edinmek için doğru bir yöntem <u>değildir</u>?</b>
        </div>
    """, unsafe_allow_html=True)

    # Şık Seçimi (Butonlar artık st.session_state günceller)
    colA, colB, colC, colD = st.columns(4)
    with colA: 
        if st.button("A", key="A"): st.session_state.selected_answer = "A"
    with colB: 
        if st.button("B", key="B"): st.session_state.selected_answer = "B"
    with colC: 
        if st.button("C", key="C"): st.session_state.selected_answer = "C"
    with colD: 
        if st.button("D", key="D"): st.session_state.selected_answer = "D"

    # Hangi şıkkın seçildiğini gösteren geri bildirim
    if st.session_state.selected_answer:
        st.info(f"Seçilen Şık: {st.session_state.selected_answer}")

    # Alt Navigasyon (Sonraki Soru Butonu Aktif)
    st.write("---")
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1: st.button("⚠️")
    with f_col2: st.button("❤️")
    with f_col3: 
        # SONRAKİ SORU BUTONU
        if st.button("➡️"): 
            if st.session_state.q_index < 14:
                next_question()
            else:
                st.success("Test Bitti!")
                if st.button("Sonuçları Gör"): change_page('test_listesi')
    with f_col4: 
        if st.button("❌"): change_page('test_listesi')

# SABİT ALT NAVİGASYON
st.markdown("""
    <div class="nav-bar">
        <span>🏠</span><span>📋</span><span>📊</span><span>❤️</span><span>◀️</span>
    </div>
    """, unsafe_allow_html=True)
