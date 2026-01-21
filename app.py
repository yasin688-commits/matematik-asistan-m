import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="5. Sınıf Test Paneli", layout="centered")

# Gelişmiş CSS (3. Adım Tasarımı İçin)
st.markdown("""
    <style>
    .main { background-color: #001C30; }
    
    /* Test Kartı Tasarımı */
    .test-card {
        background-color: #8BC34A; /* Görseldeki yeşil tonu */
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 15px;
        color: #102A43;
    }
    
    .test-title {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 5px;
    }

    .stats-container {
        display: flex;
        justify-content: space-around;
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 5px;
        margin-top: 10px;
        text-align: center;
    }

    .stat-box { font-size: 12px; font-weight: bold; }
    .stat-val { font-size: 16px; display: block; }

    /* Yeniden Çöz Butonu */
    .stButton>button {
        border-radius: 20px;
    }
    
    .header-style {
        color: white;
        padding: 10px;
        border-bottom: 1px solid #444;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Oturum Yönetimi
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- FONKSİYON: TEST KARTI OLUŞTURUCU ---
def draw_test_card(title, q_count, correct, wrong, score):
    with st.container():
        # HTML ile görsel yapıyı kuruyoruz
        st.markdown(f"""
            <div class="test-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div class="test-title">📋 {title}</div>
                        <div style="font-size: 13px;">✓ İstatistiklerim</div>
                        <div class="stats-container">
                            <div class="stat-box"><span class="stat-val">{q_count}</span>SORU</div>
                            <div class="stat-box"><span class="stat-val">{correct}</span>DOĞRU</div>
                            <div class="stat-box"><span class="stat-val">{wrong}</span>YANLIŞ</div>
                            <div class="stat-box"><span class="stat-val">{score}</span>Puan</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Sağ taraftaki "Yeniden Çöz" butonunu Streamlit butonu olarak ekliyoruz
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button(f"🔄 Yeniden Çöz", key=title):
                st.write(f"{title} başlatılıyor...")

# --- EKRANLAR ---

# 1. Ana Sayfa ve 2. Kategoriler kısmını önceki kodlardan koruyoruz...
# (Basitleştirmek için doğrudan 3. adıma odaklanalım)

if st.session_state.page == 'home':
    st.title("4. Sınıf Testleri")
    if st.button("Testlere Git"):
        st.session_state.page = 'test_listesi'
        st.rerun()

elif st.session_state.page == 'test_listesi':
    # Üst Bilgi
    st.markdown('<div class="header-style">Güneş, Dünya ve Ay</div>', unsafe_allow_html=True)
    
    # Test Verileri (Örnek)
    draw_test_card("Güneş'in Yapısı ve Özellikleri Test 1", 14, 12, 2, 85)
    draw_test_card("Güneş'in Yapısı ve Özellikleri Test 2", 12, 9, 3, 75)
    draw_test_card("Ay'ın Yapısı ve Özellikleri Test 1", 14, 11, 3, 78)
    draw_test_card("Ay'ın Yapısı ve Özellikleri Test 2", 14, 9, 5, 64)

    if st.button("⬅️ Geri Dön"):
        st.session_state.page = 'home'
        st.rerun()

# Alt Navigasyon Barı
st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background: white; padding: 10px; display: flex; justify-content: space-around; border-top: 1px solid #ccc;">
        <span style="font-size: 25px;">🏠</span>
        <span style="font-size: 25px;">📋</span>
        <span style="font-size: 25px;">📈</span>
        <span style="font-size: 25px;">❤️</span>
        <span style="font-size: 25px; color: blue;">⬅️</span>
    </div>
    """, unsafe_allow_html=True)
