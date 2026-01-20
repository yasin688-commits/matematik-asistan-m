import streamlit as st
import PyPDF2
import random

# Sayfa Ayarları
st.set_page_config(page_title="5. Sınıf Başarı Paneli", page_icon="🎓")

# Puan Durumu İlklendirme (Hafızada tutmak için)
if 'correct' not in st.session_state:
    st.session_state.correct = 0
if 'wrong' not in st.session_state:
    st.session_state.wrong = 0
if 'last_s1' not in st.session_state:
    st.session_state.last_s1 = random.randint(10, 99)
if 'last_s2' not in st.session_state:
    st.session_state.last_s2 = random.randint(10, 99)

# Stil Ayarları
st.markdown("""
    <style>
    .main { background-color: #f0f8ff; }
    .stButton>button { border-radius: 10px; width: 100%; height: 50px; font-weight: bold; }
    .score-box { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 2px solid #4CAF50; text-align: center; }
    h1 { color: #2e8b57; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Matematik & PDF Asistanı")

# --- YAN MENÜ: PUAN DURUMU ---
st.sidebar.markdown(f"""
<div class="score-box">
    <h3>📊 Puan Durumu</h3>
    <p style='color: green; font-size: 20px;'>✅ Doğru: {st.session_state.correct}</p>
    <p style='color: red; font-size: 20px;'>❌ Yanlış: {st.session_state.wrong}</p>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Puanları Sıfırla"):
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.rerun()

# --- BÖLÜM 1: PDF ÇALIŞMASI ---
st.header("📄 PDF'den Soru ve Özet")
uploaded_file = st.file_uploader("Ders notunu yükle", type="pdf")

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in pdf_reader.pages])
    
    col_pdf1, col_pdf2 = st.columns(2)
    if col_pdf1.button("📝 Özet Çıkart"):
        st.info(f"📖 **Özet:** {text[:500]}...")
    if col_pdf2.button("❓ Soru Üret"):
        st.warning("✍️ **Soru:** Bu konudaki en önemli 3 kuralı kendi kelimelerinle açıklar mısın?")

# --- BÖLÜM 2: MATEMATİK TESTİ ---
st.divider()
st.header("🔢 Hızlı Matematik Testi")

s1 = st.session_state.last_s1
s2 = st.session_state.last_s2

st.subheader(f"Soru: {s1} + {s2} = ?")
cevap = st.number_input("Cevabını buraya yaz:", step=1, key="math_input")

col1, col2 = st.columns(2)

if col1.button("✅ Kontrol Et"):
    if cevap == (s1 + s2):
        st.success(f"Harika! {s1+s2} doğru cevap! 🌟")
        st.session_state.correct += 1
    else:
        st.error(f"Maalesef yanlış. Doğru cevap {s1 + s2} olmalıydı. ❌")
        st.session_state.wrong += 1
    
    # Yeni soru hazırla
    st.session_state.last_s1 = random.randint(10, 99)
    st.session_state.last_s2 = random.randint(10, 99)
    st.button("Sonraki Soruya Geç ➡️")

if col2.button("📊 Testi Bitir / Karne Gör"):
    toplam = st.session_state.correct + st.session_state.wrong
    if toplam > 0:
        st.markdown("---")
        st.header("🏁 TEST SONUCU")
        st.write(f"**Toplam Soru:** {toplam}")
        st.success(f"**Doğru:** {st.session_state.correct}")
        st.error(f"**Yanlış:** {st.session_state.wrong}")
        
        basari_orani = (st.session_state.correct / toplam) * 100
        st.progress(basari_orani / 100)
        st.write(f"**Başarı Oranı:** %{basari_orani:.1f}")
        
        if basari_orani >= 70:
            st.balloons()
            st.success("Mükemmel gidiyorsun! 🏆")
    else:
        st.warning("Henüz hiç soru çözmedin.")
