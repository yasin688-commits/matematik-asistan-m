import streamlit as st
import time

# Sayfa Ayarları
st.set_page_config(page_title="Eğitim Uygulaması v4", layout="centered")

# --- TÜM GÖRSEL TASARIM (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #001C30; }
    
    /* Üst Bilgi Barı (Soru Ekranı) */
    .quiz-header {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: #1a3a5a;
        padding: 10px;
        border-radius: 10px;
        color: white;
        margin-bottom: 10px;
    }
    .score-badge { padding: 5px 15px; border-radius: 15px; font-weight: bold; }
    .correct-bg { background-color: #4CAF50; } /* Yeşil */
    .wrong-bg { background-color: #F44336; }   /* Kırmızı */

    /* Soru Kutusu */
    .question-container {
        background-color: white;
        color: black;
        padding: 20px;
        border-radius: 5px;
        font-family: 'Arial';
        line-height: 1.5;
        margin-bottom: 20px;
        border-bottom: 4px solid #ddd;
    }

    /* Cevap Butonları (A, B, C, D) */
    .answer-row { display: flex; justify-content: space-between; gap: 5px; margin-top: 20px; }
    .ans-btn { flex: 1; height: 50px; border-radius: 10px; font-weight: bold; border: 2px solid #ccc; }

    /* Navigasyon Barı */
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; border-top: 1px solid #ccc; z-index: 100; }
    
    /* Kategori ve Kart Tasarımları */
    .test-card { background-color: #8BC34A; border-radius: 20px; padding: 15px; margin-bottom: 10px; color: #102A43; }
    .cat-btn button { background-color: #FF8A80 !important; color: #102A43 !important; height: 60px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- OTURUM YÖNETİMİ ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'q_index' not in st.session_state: st.session_state.q_index = 1
if 'corrects' not in st.session_state: st.session_state.corrects = 4
if 'wrongs' not in st.session_state: st.session_state.wrongs = 10

def change_page(target):
    st.session_state.page = target
    st.rerun()

# --- SAYFA İÇERİKLERİ ---

# 1. ADIM: ANA SAYFA
if st.session_state.page == 'home':
    st.markdown('<h3 style="color:white; text-align:center;">4. Sınıf Testleri</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝\nTestler"): change_page('kategoriler')
        if st.button("🎬\nVideolar"): pass
    with col2:
        if st.button("❓\nRastgele"): pass
        if st.button("❤️\nFavoriler"): pass
    with col3:
        if st.button("📖\nKonu"): pass
        if st.button("❌\nHesap Sil"): pass
    st.button("🚫 Reklamları Kaldır", use_container_width=True)

# 2. ADIM: KATEGORİLER
elif st.session_state.page == 'kategoriler':
    st.markdown('<h3 style="color:white;">KATEGORİLER</h3>', unsafe_allow_html=True)
    for ders in ["Matematik", "Türkçe", "Fen Bilimleri", "Sosyal Bilgiler"]:
        st.markdown('<div class="cat-btn">', unsafe_allow_html=True)
        if st.button(f"📚 {ders}", key=ders): change_page('test_listesi')
        st.markdown('</div>', unsafe_allow_html=True)
    if st.button("⬅️ Geri"): change_page('home')

# 3. ADIM: TEST LİSTESİ
elif st.session_state.page == 'test_listesi':
    st.markdown('<h3 style="color:white;">Güneş, Dünya ve Ay</h3>', unsafe_allow_html=True)
    st.markdown(f"""<div class="test-card"><b>📋 Güneş'in Yapısı Test 1</b><br>14 Soru | Puan: 85</div>""", unsafe_allow_html=True)
    if st.button("🔄 Yeniden Çöz"): change_page('quiz')
    if st.button("⬅️ Geri"): change_page('kategoriler')

# 4. ADIM: SORU ÇÖZME EKRANI (YENİ GÖRSELE GÖRE)
elif st.session_state.page == 'quiz':
    # Üst Bilgi Barı: Zaman, Soru Sayısı, Skor
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
    st.markdown("""
        <div class="question-container">
            Güneş ile ilgili bilgi edinebilmek için bazı yöntemlerden yararlanılır.<br><br>
            <b>Aşağıdakilerden hangisi Güneş ile ilgili bilgi edinmek için doğru ve uygun bir yöntem <u>değildir</u>?</b><br><br>
            A) Uzaydaki teleskopların çekmiş olduğu Güneş fotoğraflarını incelemek<br>
            B) Güneş'in aylara ve mevsimlere göre aldığı konumları karşılaştırmak<br>
            C) Büyüteç ve benzeri merceklerle Güneş'e doğrudan bakmak<br>
            D) Güneş'e yakın uçuş gerçekleştirebilecek donanımda uzay araçları tasarlayıp göndermek
        </div>
    """, unsafe_allow_html=True)

    # Reklam Alanı (Görseldeki mobilya reklamı temsili)
    st.info("📺 Reklam Alanı")

    # Alt Cevap Butonları (A, B, C, D)
    colA, colB, colC, colD = st.columns(4)
    with colA: st.button("A", key="btnA", use_container_width=True)
    with colB: st.button("B", key="btnB", use_container_width=True) # Görselde B kırmızı
    with colC: st.button("C", key="btnC", use_container_width=True) # Görselde C yeşil
    with colD: st.button("D", key="btnD", use_container_width=True)

    # Alt Fonksiyonel Bar (Ünlem, Kalp, Ok, X)
    st.write("---")
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1: st.button("⚠️")
    with f_col2: st.button("❤️")
    with f_col3: 
        if st.button("➡️"): 
            st.session_state.q_index += 1
            st.rerun()
    with f_col4: 
        if st.button("❌"): change_page('test_listesi')

# --- SABİT ALT NAVİGASYON ---
st.markdown("""
    <div class="nav-bar">
        <span>🏠</span><span>📋</span><span>📊</span><span>❤️</span><span>◀️</span>
    </div>
    """, unsafe_allow_html=True)
