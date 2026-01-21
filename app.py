import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="5. Sınıf Tüm Dersler", layout="centered")

# Görseldeki Mobile Yakın Tasarım İçin CSS
st.markdown("""
    <style>
    .main {
        background-color: #001C30;
    }
    .stButton>button {
        width: 100%;
        height: 100px;
        border-radius: 15px;
        border: none;
        color: black;
        font-weight: bold;
        font-size: 16px;
    }
    /* Kart Renkleri */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button { background-color: #90CAF9; } /* Mavi */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button { background-color: #A5D6A7; } /* Yeşil */
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) button { background-color: #EF9A9A; } /* Kırmızı */
    
    .header-text {
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Başlık
st.markdown('<p class="header-text">4. Sınıf Testleri</p>', unsafe_allow_html=True)

# 3x3 Izgara Yapısı (Grid)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝\nTestler"):
        st.info("Testler Sayfası Hazırlanıyor...")
    if st.button("🎬\nVideolar"):
        st.info("Videolar Sayfası Hazırlanıyor...")
    if st.button("🎮\nEğitici Oyunlar"):
        st.info("Oyunlar Sayfası Hazırlanıyor...")

with col2:
    if st.button("❓\nRastgele Mod"):
        st.info("Rastgele Sorular Getiriliyor...")
    if st.button("❤️\nFavori Sorular"):
        st.info("Favorileriniz...")
    if st.button("📅\nÖnemli Günler"):
        st.info("Takvim Açılıyor...")

with col3:
    if st.button("📖\nKonu Anlatımı"):
        st.info("Konu Listesi...")
    if st.button("📊\nİstatistiklerim"):
        st.info("Başarı Durumunuz...")
    if st.button("❌\nHesabımı Sil"):
        st.warning("Emin misiniz?")

st.write("---")

# Reklamları Kaldır Butonu
if st.button("🚫 Reklamları Kaldır", use_container_width=True):
    st.success("Premium üyelik sayfasına yönlendiriliyorsunuz...")

# Alt Navigasyon (Simüle edilmiş)
st.markdown("""
    <div style="background-color: white; padding: 10px; border-radius: 10px; display: flex; justify-content: space-around;">
        <span style="color: blue; font-size: 20px;">🏠</span>
        <span style="font-size: 20px;">📋</span>
        <span style="font-size: 20px;">⏹️</span>
        <span style="font-size: 20px;">⭐</span>
    </div>
    """, unsafe_allow_html=True)
