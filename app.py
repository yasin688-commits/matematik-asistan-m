import streamlit as st
import PyPDF2
import random

st.set_page_config(page_title="5. Sınıf Başarı Paneli", page_icon="🎓")

st.markdown("""
    <style>
    .main { background-color: #f0f8ff; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 10px; width: 100%; }
    h1 { color: #2e8b57; font-family: 'Comic Sans MS'; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 5. Sınıf Matematik & PDF Asistanı")

# Yan Menü
st.sidebar.header("📅 Günlük Program")
st.sidebar.info("1. Matematik (45 dk)\n2. Mola (15 dk)\n3. PDF Çalışması (30 dk)")

# PDF Bölümü
st.header("📄 PDF'den Soru ve Özet")
uploaded_file = st.file_uploader("PDF Yükle", type="pdf")

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in pdf_reader.pages])
    
    secim = st.radio("Ne yapalım?", ["Özet Çıkart", "Soru Üret"])
    if st.button("Başlat"):
        if secim == "Özet Çıkart":
            st.info(text[:500] + "...")
        else:
            st.warning("Bu konudaki en önemli 3 tanımı kendi cümlelerinle yazar mısın?")

# Matematik Alıştırması
st.divider()
st.header("🔢 Hızlı İşlem")
s1, s2 = random.randint(10, 99), random.randint(10, 99)
cevap = st.number_input(f"{s1} + {s2} sonucu kaçtır?", step=1)
if st.button("Kontrol Et"):
    if cevap == (s1 + s2):
        st.balloons()
        st.success("Harika! 🌟")
    else:
        st.error("Tekrar dene! 💪")
