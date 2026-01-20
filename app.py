import streamlit as st
import random

# =========================
# SAYFA AYARI
# =========================
st.set_page_config(
    page_title="Evde Matematik Asistanı",
    page_icon="🧮",
    layout="centered"
)

# =========================
# BAŞLIK
# =========================
st.markdown(
    """
    <h1 style='text-align:center;'>🧮 Evde Matematik Asistanı</h1>
    <p style='text-align:center;'>Çocuklar için eğlenceli matematik</p>
    """,
    unsafe_allow_html=True
)

# =========================
# SEVİYE SEÇİMİ
# =========================
seviye = st.selectbox(
    "📘 Seviye Seç",
    ["1. Sınıf", "2. Sınıf", "3. Sınıf", "4. Sınıf"]
)

# =========================
# SORU OLUŞTURMA
# =========================
def soru_uret(seviye):
    if seviye == "1. Sınıf":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        return f"{a} + {b}", a + b

    if seviye == "2. Sınıf":
        a = random.randint(10, 50)
        b = random.randint(1, 20)
        return f"{a} - {b}", a - b

    if seviye == "3. Sınıf":
        a = random.randint(2, 10)
        b = random.randint(2, 10)
        return f"{a} × {b}", a * b

    if seviye == "4. Sınıf":
        b = random.randint(2, 10)
        c = random.randint(2, 10)
        a = b * c
        return f"{a} ÷ {b}", c


# =========================
# SESSION STATE
# =========================
if "soru" not in st.session_state:
    st.session_state.soru, st.session_state.cevap = soru_uret(seviye)
    st.session_state.puan = 0

# =========================
# SORU GÖSTER
# =========================
st.markdown(
    f"<h2 style='text-align:center;'>❓ {st.session_state.soru}</h2>",
    unsafe_allow_html=True
)

# =========================
# CEVAP AL
# =========================
kullanici_cevap = st.number_input(
    "Cevabını yaz",
    step=1,
    format="%d"
)

# =========================
# KONTROL BUTONU
# =========================
if st.button("✅ Kontrol Et"):
    if kullanici_cevap == st.session_state.cevap:
        st.success("🎉 Tebrikler! Doğru cevap")
        st.session_state.puan += 10
    else:
        st.error(f"❌ Yanlış. Doğru cevap: {st.session_state.cevap}")

    st.session_state.soru, st.session_state.cevap = soru_uret(seviye)

# =========================
# PUAN
# =========================
st.markdown(
    f"<h3 style='text-align:center;'>⭐ Puan: {st.session_state.puan}</h3>",
    unsafe_allow_html=True
)

# =========================
# YENİDEN BAŞLAT
# =========================
if st.button("🔄 Yeniden Başlat"):
    st.session_state.clear()
    st.experimental_rerun()

# =========================
# ALT BİLGİ
# =========================
st.markdown(
    """
    <hr>
    <p style='text-align:center; font-size:13px;'>
    Evde çocuklar için güvenli matematik uygulaması
    </p>
    """,
    unsafe_allow_html=True
)
