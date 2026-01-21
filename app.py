import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="5. Sınıf Tüm Dersler", layout="centered")

# CSS ile Görseldeki Tasarımı Bire Bir Uygulama
st.markdown("""
    <style>
    .main { background-color: #001C30; }
    
    /* Kategori Kart Tasarımı */
    .category-card {
        background-color: #FF8A80; /* Görseldeki kırmızı/somon tonu */
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        color: #102A43;
        text-decoration: none;
        cursor: pointer;
        border: none;
    }
    .category-icon { font-size: 35px; margin-right: 15px; }
    .category-text { font-weight: bold; font-size: 20px; }
    .category-subtext { font-size: 14px; color: white; display: block; }

    /* Başlık Stili */
    .header-text {
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 10px 0;
        border-bottom: 2px solid #333;
        margin-bottom: 20px;
    }
    
    /* Navigasyon Barı */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        border-top-left-radius: 20px;
        border-top-right-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sayfa Yönetimi (Navigasyon)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- FONKSİYON: KATEGORİ KARTI OLUŞTURMA ---
def category_item(icon, title):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<div style='font-size:40px; text-align:center; padding-top:10px;'>{icon}</div>", unsafe_allow_html=True)
    with col2:
        if st.button(f"{title}\n\n✓ Kategori", key=title, use_container_width=True):
            st.session_state.page = f"test_{title}"
            st.rerun()

# --- EKRAN 1: ANA SAYFA (GRID) ---
if st.session_state.page == 'home':
    st.markdown('<p style="color:white; text-align:center; font-size:24px;">4. Sınıf Testleri</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝\nTestler"):
            st.session_state.page = 'kategoriler'
            st.rerun()
    # (Diğer ana sayfa butonlarını buraya ekleyebilirsin...)
    st.write("Ana sayfadaki 'Testler' butonuna basarak kategorilere geçebilirsin.")

# --- EKRAN 2: KATEGORİLER (LİSTE) ---
elif st.session_state.page == 'kategoriler':
    st.markdown('<p class="header-text">KATEGORİLER</p>', unsafe_allow_html=True)

    # Kategori Listesi (Görseldeki Sırayla)
    category_item("📐", "Matematik")
    category_item("📚", "Türkçe")
    category_item("🧪", "Fen Bilimleri")
    category_item("🌍", "Sosyal Bilgiler")
    category_item("🇬🇧", "İngilizce")
    category_item("🕌", "Din Kültürü")

    # Geri Dönüş ve Alt Navigasyon
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("⬅️ Ana Sayfaya Dön"):
        st.session_state.page = 'home'
        st.rerun()

# --- ALT NAVİGASYON (Tüm sayfalarda görünür) ---
st.markdown("""
    <div class="nav-bar">
        <span>🏠</span>
        <span>📋</span>
        <span>📊</span>
        <span>❤️</span>
        <span>◀️</span>
    </div>
    """, unsafe_allow_html=True)
