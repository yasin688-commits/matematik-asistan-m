import streamlit as st
import random

# --------------------
# SAYFA AYARI
# --------------------
st.set_page_config(
    page_title="Evde Matematik Asistanı",
    page_icon="🧮",
    layout="centered"
)

# --------------------
# SESSION STATE
# --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "score" not in st.session_state:
    st.session_state.score = 0

if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.answer = None

# --------------------
# STİL
# --------------------
st.markdown("""
<style>
body {
    background-color: #f4f6fb;
}
.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    cursor: pointer;
}
.card:hover {
    background: #eef2ff;
}
.big {
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --------------------
# FONKSİYONLAR
# --------------------
def new_question(level):
    if level == "4. Sınıf":
        a = random.randint(1, 20)
        b = random.randint(1, 20)
    else:
        a = random.randint(10, 50)
        b = random.randint(10, 50)

    st.session_state.question = f"{a} + {b}"
    st.session_state.answer = a + b

# --------------------
# ANA SAYFA
# --------------------
if st.session_state.page == "home":
    st.title("🧮 Evde Matematik Asistanı")
    st.caption("Çocuklar için eğlenceli ve güvenli matematik")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 Testler"):
            st.session_state.page = "test"

    with col2:
        if st.button("🎲 Rastgele Mod"):
            st.session_state.page = "test"

    with col3:
        if st.button("📊 İstatistik"):
            st.session_state.page = "stats"

    st.markdown("---")
    st.info("Reklamsız – güvenli – ev ortamına uygun")

# --------------------
# TEST SAYFASI
# --------------------
elif st.session_state.page == "test":
    st.title("📝 Matematik Testi")

    level = st.selectbox("Seviye Seç", ["4. Sınıf", "5. Sınıf"])

    if st.session_state.question is None:
        new_question(level)

    st.subheader(f"❓ {st.session_state.question}")

    user_answer = st.number_input("Cevabını yaz", step=1)

    if st.button("✅ Kontrol Et"):
        if user_answer == st.session_state.answer:
            st.success("🎉 Doğru!")
            st.session_state.score += 10
        else:
            st.error(f"❌ Yanlış! Doğru cevap: {st.session_state.answer}")

        st.session_state.question = None

    st.markdown(f"⭐ **Puan:** {st.session_state.score}")

    if st.button("🔄 Yeniden Başlat"):
        st.session_state.score = 0
        st.session_state.question = None

    if st.button("⬅️ Ana Sayfa"):
        st.session_state.page = "home"

# --------------------
# İSTATİSTİK
# --------------------
elif st.session_state.page == "stats":
    st.title("📊 İstatistikler")

    st.metric("Toplam Puan", st.session_state.score)

    if st.button("⬅️ Ana Sayfa"):
        st.session_state.page = "home"
