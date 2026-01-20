import streamlit as st
import random
import json
import pandas as pd

# =========================
# OPENAI
# =========================
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# =========================
# SAYFA AYARI
# =========================
st.set_page_config(
    page_title="Yusuf AI – Evde Akıllı Öğrenme",
    page_icon="🧠",
    layout="wide"
)

# =========================
# MODERN TASARIM
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg,#F8FAFC,#EEF2FF); }

.card {
    background: rgba(255,255,255,0.85);
    border-radius: 22px;
    padding: 30px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.06);
}

.stat {
    background: linear-gradient(135deg,#6366F1,#8B5CF6);
    color: white;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# =========================
# SESSION STATE
# =========================
state = st.session_state
state.setdefault("puan", 0)
state.setdefault("history", [])
state.setdefault("mistakes", [])
state.setdefault("current_q", None)
state.setdefault("test_active", False)


# =========================
# ZORLUK AYARLAMA
# =========================
def adjust_difficulty(history):
    if len(history) < 3:
        return "orta"
    last = history[-3:]
    d = last.count("Doğru")
    if d == 3:
        return "zor"
    if d <= 1:
        return "kolay"
    return "orta"


# =========================
# YAPAY ZEKA SORU ÜRETİMİ
# =========================
def generate_ai_question(grade=5, difficulty="orta"):
    topic = random.choice([
        "Kesirler",
        "Basamak Değeri",
        "Yol Problemleri",
        "Yüzdeler"
    ])

    prompt = f"""
    Sen {grade}. sınıf matematik öğretmenisin.

    Konu: {topic}
    Zorluk: {difficulty}

    ŞARTLAR:
    - Günlük hayatla ilişkili
    - Ezbere dayalı olmasın
    - 4 şıklı
    - Tek doğru cevap
    - Yanlış şıklar mantıklı olsun

    SADECE JSON ÇIKTI VER:

    {{
      "konu": "{topic}",
      "soru": "",
      "siklar": ["A","B","C","D"],
      "cevap": "",
      "adimlar": ["", "", ""]
    }}
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(r.choices[0].message.content)


# =========================
# YANLIŞ ANALİZİ
# =========================
def analyze_mistakes(mistakes):
    result = {}
    for m in mistakes:
        result[m["konu"]] = result.get(m["konu"], 0) + 1
    return result


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"""
    <div class="stat">
        🏆 PUAN
        <h1>{state.puan}</h1>
    </div>
    """, unsafe_allow_html=True)

    if state.history:
        df = pd.DataFrame({
            "Durum": state.history
        })
        st.bar_chart(df["Durum"].value_counts())


# =========================
# ANA AKIŞ
# =========================
st.title("🧠 Yusuf AI – Evde Akıllı Öğrenme")

if not state.test_active:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("👶 Evde çocuklar için **yapay zeka destekli matematik öğrenme**")

    if st.button("🚀 Günlük Göreve Başla", use_container_width=True):
        state.test_active = True
        state.puan = 0
        state.history = []
        state.mistakes = []
        state.current_q = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


else:
    if state.current_q is None:
        level = adjust_difficulty(state.history)
        state.current_q = generate_ai_question(grade=5, difficulty=level)

    q = state.current_q

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.caption(f"Konu: {q['konu']}")
    st.subheader(q["soru"])

    for s in q["siklar"]:
        if st.button(s, use_container_width=True):
            correct = s == q["cevap"]
            state.history.append("Doğru" if correct else "Yanlış")

            if correct:
                state.puan += 20
            else:
                state.mistakes.append(q)

            state.current_q = None
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # RAPOR
    if len(state.history) >= 5:
        st.divider()
        st.header("📊 Veli Raporu")

        analysis = analyze_mistakes(state.mistakes)
        if analysis:
            for konu, adet in analysis.items():
                st.write(f"❌ {konu}: {adet} hata")
        else:
            st.success("🎉 Tüm konular güçlü!")

        if st.button("🔄 Tekrar Başla"):
            state.test_active = False
            st.rerun()
