import streamlit as st
import PyPDF2
import random

# Sayfa Ayarları
st.set_page_config(page_title="Yusuf Agaç Matematik Paneli", page_icon="🚀")

# Puan Durumu İlklendirme
if 'correct' not in st.session_state:
    st.session_state.correct = 0
if 'wrong' not in st.session_state:
    st.session_state.wrong = 0
if 'last_s1' not in st.session_state:
    st.session_state.last_s1 = random.randint(5, 20)
if 'last_s2' not in st.session_state:
    st.session_state.last_s2 = random.randint(2, 12)
if 'islem_turu' not in st.session_state:
    st.session_state.islem_turu = "+"

# Stil Ayarları
st.markdown("""
    <style>
    .main { background-color: #fdf6e3; }
    .stButton>button { border-radius: 12px; width: 100%; font-size: 18px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #ffd700; color: black; }
    .score-box { background: linear-gradient(to right, #11998e, #38ef7d); padding: 15px; border-radius: 15px; color: white; text-align: center; }
    h1 { color: #d35400; text-align: center; font-family: 'Trebuchet MS'; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Yusuf Agaç Matematik Programı")

# --- YAN MENÜ: YUSUF'UN SKOR TABELASI ---
st.sidebar.markdown(f"""
<div class="score-box">
    <h2>🏆 Yusuf'un Karnesi</h2>
    <p style='font-size: 24px;'>✅ Doğru: {st.session_state.correct}</p>
    <p style='font-size: 24px;'>❌ Yanlış: {st.session_state.wrong}</p>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Puanları Sıfırla"):
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.rerun()

# --- BÖLÜM 1: PDF ÇALIŞMA ALANI ---
st.header("📄 PDF Çalışma Alanı")
uploaded_file = st.file_uploader("PDF Dosyanı Yükle Yusuf", type="pdf")

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in pdf_reader.pages])
    
    col_pdf1, col_pdf2 = st.columns(2)
    if col_pdf1.button("📝 Özet Hazırla"):
        st.info(f"📚 **Yusuf, işte notlarının özeti:**\n\n {text[:600]}...")
    if col_pdf2.button("❓ Soru Çıkart"):
        st.warning("🤔 **Soru:** PDF'de anlatılan en önemli konu sence nedir? Cevabı notlarına yaz!")

# --- BÖLÜM 2: MATEMATİK TESTİ (Çoktan Seçmeli İşlem) ---
st.divider()
st.header("🔢 Matematik Antrenmanı")

islem = st.selectbox("Hangi işlemi çalışmak istersin?", ["Toplama", "Çıkarma", "Çarpma"])

# Yeni Soru Üretme Fonksiyonu
def yeni_soru():
    if islem == "Toplama":
        st.session_state.last_s1 = random.randint(10, 100)
        st.session_state.last_s2 = random.randint(10, 100)
        st.session_state.islem_turu = "+"
    elif islem == "Çıkarma":
        st.session_state.last_s1 = random.randint(50, 100)
        st.session_state.last_s2 = random.randint(1, 49)
        st.session_state.islem_turu = "-"
    elif islem == "Çarpma":
        st.session_state.last_s1 = random.randint(2, 15)
        st.session_state.last_s2 = random.randint(2, 10)
        st.session_state.islem_turu = "x"

s1 = st.session_state.last_s1
s2 = st.session_state.last_s2
tür = st.session_state.islem_turu

st.subheader(f"Soru: {s1} {tür} {s2} = ?")
cevap = st.number_input("Cevabını buraya yaz:", step=1, key="math_input")

if st.button("Sonucu Kontrol Et"):
    dogru_cevap = 0
    if tür == "+": dogru_cevap = s1 + s2
    elif tür == "-": dogru_cevap = s1 - s2
    elif tür == "x": dogru_cevap = s1 * s2
    
    if cevap == dogru_cevap:
        st.balloons()
        st.success(f"Tebrikler Yusuf! ✅ {dogru_cevap} doğru cevap.")
        st.session_state.correct += 1
    else:
        st.error(f"Hadi bir daha dene Yusuf! ❌ Doğru cevap {dogru_cevap} olmalıydı.")
        st.session_state.wrong += 1
    
    yeni_soru()
    st.button("Yeni Soruya Geç")

# --- BÖLÜM 3: KARNE ---
if st.button("🏁 Çalışmayı Bitir ve Karneyi Gör"):
    toplam = st.session_state.correct + st.session_state.wrong
    if toplam > 0:
        st.markdown("---")
        st.header("📊 Bugünün Başarı Tablosu")
        st.write
