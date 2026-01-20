import random
from datetime import datetime

import streamlit as st

# --------------------
# SAYFA AYARI
# --------------------
st.set_page_config(
    page_title="Evde Matematik Asistanı",
    page_icon="🧠",
    layout="wide"
)


# --------------------
# GENEL STİL
# --------------------
custom_css = """
<style>
/* Genel arka plan */
.stApp {
    background: linear-gradient(135deg, #f5f7ff 0%, #e3f2fd 50%, #fce4ec 100%);
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Kart tasarımı */
.card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 18px;
    padding: 24px 26px;
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.12);
    border: 1px solid rgba(148, 163, 184, 0.2);
}

.card-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 0.3rem;
}

.card-subtitle {
    font-size: 0.86rem;
    color: #6b7280;
    margin-bottom: 0.8rem;
}

.question-text {
    font-size: 1.05rem;
    line-height: 1.6;
    color: #111827;
}

.tag {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 500;
    background: #eef2ff;
    color: #4338ca;
    border: 1px solid #c7d2fe;
}

.difficulty-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
}

.difficulty-1 {
    background: #ecfdf3;
    color: #15803d;
    border: 1px solid #bbf7d0;
}

.difficulty-2 {
    background: #fffbeb;
    color: #b45309;
    border: 1px solid #fed7aa;
}

.difficulty-3 {
    background: #fef2f2;
    color: #b91c1c;
    border: 1px solid #fecaca;
}

.metric-number {
    font-size: 1.7rem;
    font-weight: 700;
    color: #0f172a;
}

.metric-label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6b7280;
}

.footer-text {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 1.5rem;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


# --------------------
# SESSION STATE
# --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "score" not in st.session_state:
    st.session_state.score = 0

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0

if "question_data" not in st.session_state:
    st.session_state.question_data = None

if "history" not in st.session_state:
    st.session_state.history = []


# --------------------
# SORU ÜRETİCİLER
# --------------------
def generate_4th_grade_question(topic: str):
    """4. sınıf için farklı konu tiplerinde yeni nesil soru üretir."""
    if topic == "Toplama / Çıkarma":
        variant = random.choice([1, 2, 3])
        difficulty = 1 if variant in (1, 2) else 2

        if variant == 1:
            a = random.randint(30, 95)
            b = random.randint(10, 65)
            c = random.randint(5, 35)

            question = (
                f"Bir kırtasiyede sabah {a} tane kalem satılıyor. "
                f"Öğleden sonra sabah satılandan {b} tane daha az kalem satılıyor. "
                f"Gün sonunda depoda {c} kalem kaldığına göre, bu kırtasiyede başlangıçta kaç kalem vardı?"
            )

            sold_morning = a
            sold_afternoon = a - b
            total_sold = sold_morning + sold_afternoon
            answer = total_sold + c

            explanation = (
                f"Sabah satılan: {sold_morning} kalem\n"
                f"Öğleden sonra satılan: {sold_afternoon} kalem\n"
                f"Toplam satılan: {sold_morning} + {sold_afternoon} = {total_sold} kalem\n"
                f"Depoda kalan: {c} kalem\n"
                f"Başlangıçtaki miktar: {total_sold} + {c} = {answer} kalem"
            )

        elif variant == 2:
            a = random.randint(120, 280)
            b = random.randint(40, 110)
            c = random.randint(20, 90)

            question = (
                f"Bir okulun kütüphanesine önce {a} kitap alındı. "
                f"Daha sonra {b} kitap daha eklendi. "
                f"Bir süre sonra {c} kitap başka bir okula gönderildi.\n\n"
                f"Buna göre kütüphanede kaç kitap kalmıştır?"
            )
            answer = a + b - c
            explanation = (
                f"Önceki kitap sayısı: {a}\n"
                f"Eklenen kitap: {b} → {a} + {b} = {a + b}\n"
                f"Gönderilen kitap: {c} → {a + b} - {c} = {answer}"
            )

        else:
            a = random.randint(80, 160)
            b = random.randint(20, 60)
            c = random.randint(15, 55)

            question = (
                f"Bir markette {a} litre süt vardı. "
                f"Sabah {b} litre süt satıldı. "
                f"Öğleden sonra {c} litre süt daha satıldı.\n\n"
                f"Marketin elinde kaç litre süt kalmıştır?"
            )
            answer = a - b - c
            explanation = (
                f"Başlangıç: {a} litre\n"
                f"Sabah satılan: {b} → Kalan: {a} - {b} = {a - b}\n"
                f"Öğleden sonra satılan: {c} → Kalan: {a - b} - {c} = {answer}"
            )

    elif topic == "Çarpma / Bölme":
        variant = random.choice([1, 2, 3])
        difficulty = 1 if variant in (1, 2) else 2

        if variant == 1:
            a = random.randint(3, 9)
            b = random.randint(4, 8)
            c = random.randint(2, 4)

            question = (
                f"Bir sınıftaki her sırada {a} öğrenci oturuyor. "
                f"Sınıfta {b} sıra vardır. Okulda bu sınıftan {c} tane olduğunu biliyoruz.\n\n"
                f"Buna göre bu okuldaki bu sınıflarda toplam kaç öğrenci vardır?"
            )

            answer_one_class = a * b
            answer = answer_one_class * c
            explanation = (
                f"Bir sınıftaki öğrenci sayısı: {a} × {b} = {answer_one_class}\n"
                f"Bu sınıflardan {c} tane olduğuna göre: "
                f"{answer_one_class} × {c} = {answer}"
            )

        elif variant == 2:
            a = random.randint(4, 9)
            b = random.randint(6, 12)
            question = (
                f"Bir fırın sabah {a} tepsi kurabiye yaptı. "
                f"Her tepside {b} kurabiye olduğuna göre, toplam kaç kurabiye yapılmıştır?"
            )
            answer = a * b
            explanation = f"Toplam kurabiye: {a} × {b} = {answer}"

        else:
            total = random.randint(72, 144)
            per_box = random.choice([6, 8, 9, 12])
            question = (
                f"Bir oyuncakçıya {total} tane balon geldi. "
                f"Balonlar {per_box}'erli paketlere ayrılacaktır.\n\n"
                f"Kaç paket balon olur?"
            )
            answer = total // per_box
            explanation = f"Paket sayısı: {total} ÷ {per_box} = {answer}"

    else:  # Zihinden işlem / problem çözme
        variant = random.choice([1, 2, 3])
        difficulty = 2

        if variant == 1:
            a = random.randint(100, 250)
            b = random.randint(20, 90)
            c = random.randint(10, 60)

            question = (
                f"Ali, kütüphanedeki kitapların {b} tanesini sınıfa götürüyor. "
                f"Kütüphanede başlangıçta {a} kitap vardı. "
                f"Ertesi gün sınıftan {c} kitap geri getiriliyor.\n\n"
                f"Buna göre kütüphanede şimdi kaç kitap vardır?"
            )

            after_take = a - b
            answer = after_take + c
            explanation = (
                f"Başlangıçtaki kitap sayısı: {a}\n"
                f"Sınıfa giden: {b} kitap → Kalan: {a} - {b} = {after_take}\n"
                f"Geri gelen: {c} kitap → Son durum: {after_take} + {c} = {answer}"
            )

        elif variant == 2:
            a = random.randint(180, 360)
            b = random.randint(40, 120)
            c = random.randint(25, 95)
            question = (
                f"Bir geziye {a} kişi katıldı. "
                f"Öğle yemeğinde {b} kişi ayrıldı. "
                f"Akşam yemeğine ise öğleden sonra {c} kişi daha katıldı.\n\n"
                f"Akşam yemeğinde toplam kaç kişi vardır?"
            )
            answer = a - b + c
            explanation = (
                f"Başlangıç: {a}\n"
                f"Ayrılan: {b} → Kalan: {a} - {b} = {a - b}\n"
                f"Katılan: {c} → Son: {a - b} + {c} = {answer}"
            )

        else:
            a = random.randint(90, 210)
            b = random.randint(25, 80)
            c = random.randint(10, 50)
            question = (
                f"Bir otobüste {a} yolcu vardı. "
                f"Bir durakta {b} yolcu indi, {c} yolcu bindi.\n\n"
                f"Otobüste kaç yolcu olmuştur?"
            )
            answer = a - b + c
            explanation = f"Son yolcu sayısı: {a} - {b} + {c} = {answer}"

    return question, answer, explanation, difficulty


def generate_5th_grade_question(topic: str):
    """5. sınıf için yeni nesil, daha çok çoklu işlem içeren sorular üretir."""
    if topic == "Doğal Sayılar / İşlemler":
        variant = random.choice([1, 2, 3])
        difficulty = 2

        if variant == 1:
            a = random.randint(120, 480)
            b = random.randint(3, 9)
            c = random.randint(2, 7)

            question = (
                f"Bir fabrikada her gün eşit sayıda oyuncak üretiliyor. "
                f"Bu fabrika {b} günde toplam {a} oyuncak üretiyor.\n\n"
                f"Daha sonra üretim hızı artırılıyor ve günde üretilen oyuncak sayısı {c} katına çıkıyor.\n"
                f"Yeni üretim hızına göre bu fabrika 1 günde kaç oyuncak üretir?"
            )

            per_day = a // b
            answer = per_day * c
            explanation = (
                f"{b} günde {a} oyuncak → Günde üretilen: {a} ÷ {b} = {per_day}\n"
                f"Üretim {c} katına çıktı → Yeni hız: {per_day} × {c} = {answer}"
            )

        elif variant == 2:
            total = random.randint(240, 720)
            days = random.randint(4, 9)
            extra = random.randint(15, 60)
            question = (
                f"Bir atölye {days} günde toplam {total} parça üretiyor. "
                f"Son gün, diğer günlerden {extra} parça daha fazla üretmiştir.\n\n"
                f"Buna göre son gün kaç parça üretilmiştir?"
            )
            # (days-1)*x + (x+extra) = total => days*x + extra = total
            x = (total - extra) // days
            answer = x + extra
            explanation = (
                f"Diğer günlerin günlük üretimi x olsun.\n"
                f"({days}-1)·x + (x + {extra}) = {total} ⇒ {days}·x + {extra} = {total}\n"
                f"{days}·x = {total - extra} ⇒ x = {(total - extra)} ÷ {days} = {x}\n"
                f"Son gün: x + {extra} = {x} + {extra} = {answer}"
            )
            difficulty = 3

        else:
            a = random.randint(18, 60)
            b = random.randint(10, 40)
            c = random.randint(2, 6)
            question = (
                f"Bir okulda her sınıfta {a} öğrenci vardır. "
                f"Bu okulda {b} sınıf olduğuna göre okuldaki toplam öğrenci sayısı kaçtır?\n\n"
                f"Okul, toplam öğrenci sayısının {c} katı kadar kitap bağışı yaparsa kaç kitap bağışlar?"
            )
            total_students = a * b
            answer = total_students * c
            explanation = (
                f"Toplam öğrenci: {a} × {b} = {total_students}\n"
                f"Kitap bağışı: {total_students} × {c} = {answer}"
            )

    elif topic == "Oran / Orantı":
        variant = random.choice([1, 2, 3])
        difficulty = 3

        if variant == 1:
            a = random.randint(2, 5)
            b = a * random.randint(2, 4)  # orantılı sayı
            c = random.randint(30, 80)

            question = (
                f"Bir pastanın tarifinde {a} bardak un kullanıldığında "
                f"{c} gram şeker kullanılıyor.\n\n"
                f"Aynı oranda hazırlanmış daha büyük bir pastada {b} bardak un kullanılırsa "
                f"kaç gram şeker kullanılması gerekir?"
            )

            scale = b / a
            answer = int(c * scale)
            explanation = (
                f"Un miktarı {a} bardaktan {b} bardağa çıkıyor.\n"
                f"Oran: {b} ÷ {a} = {scale}\n"
                f"Şeker miktarı da aynı oranda artar: {c} × {scale} = {answer}"
            )

        elif variant == 2:
            x = random.randint(3, 7)
            y = random.randint(2, 6)
            a = x
            b = x * random.randint(2, 4)
            c = y * random.randint(10, 25)
            question = (
                f"Bir karışım {a}:{y} oranında hazırlanıyor. "
                f"Yani {a} ölçü A maddesine karşılık {y} ölçü B maddesi kullanılıyor.\n\n"
                f"A maddesi {b} ölçü olursa B maddesi kaç ölçü olmalıdır?"
            )
            answer = int((b / a) * y)
            explanation = (
                f"Oran sabit: A {a} ise B {y}\n"
                f"A {b} olunca çarpan: {b} ÷ {a} = {b / a}\n"
                f"B: {y} × {b / a} = {answer}"
            )

        else:
            a = random.randint(4, 10)
            b = a * random.randint(2, 5)
            c = random.randint(8, 20)
            question = (
                f"Bir araç {a} litre yakıt ile {c} km yol gidiyor.\n\n"
                f"Aynı şartlarda {b} litre yakıt ile kaç km yol gider?"
            )
            scale = b / a
            answer = int(c * scale)
            explanation = f"{b} litre, {a} litrenin {scale} katı → {c} × {scale} = {answer} km"

    else:  # Geometri / çevre - alan
        variant = random.choice([1, 2, 3])
        difficulty = 2

        if variant == 1:
            a = random.randint(80, 220)  # cm
            b = random.randint(60, 180)  # cm

            question = (
                f"Uzun kenarı {a} cm, kısa kenarı {b} cm olan dikdörtgen şeklinde "
                f"bir bahçe vardır.\n"
                f"Bahçenin etrafına 1 metre arayla fidan dikilecektir. "
                f"(1 metre = 100 cm)\n\n"
                f"Buna göre bahçenin etrafına toplam kaç fidan dikilir?"
            )

            perimeter_cm = 2 * (a + b)
            answer = perimeter_cm // 100
            explanation = (
                f"Dikdörtgenin çevresi: 2 × ({a} + {b}) = {perimeter_cm} cm\n"
                f"Her 100 cm'de (= 1 m) 1 fidan dikiliyor.\n"
                f"Toplam fidan sayısı: {perimeter_cm} ÷ 100 = {answer}"
            )

        elif variant == 2:
            a = random.randint(6, 18)  # cm
            b = random.randint(5, 16)  # cm
            question = (
                f"Kenarları {a} cm ve {b} cm olan dikdörtgenin çevresi kaç cm'dir?"
            )
            answer = 2 * (a + b)
            explanation = f"Çevre = 2 × ({a} + {b}) = {answer}"

        else:
            a = random.randint(6, 18)
            b = random.randint(5, 16)
            question = (
                f"Kenarları {a} cm ve {b} cm olan dikdörtgenin alanı kaç cm²'dir?"
            )
            answer = a * b
            explanation = f"Alan = {a} × {b} = {answer} cm²"

    return question, answer, explanation, difficulty


def generate_question(level: str, topic: str):
    if level == "4. Sınıf":
        return generate_4th_grade_question(topic)
    return generate_5th_grade_question(topic)


# --------------------
# YARDIMCI FONKSİYONLAR
# --------------------
def reset_question():
    st.session_state.question_data = None


def record_result(correct: bool, user_answer, correct_answer, level, topic, difficulty):
    st.session_state.total_questions += 1
    if correct:
        st.session_state.correct_answers += 1
        st.session_state.score += 10 * difficulty

    st.session_state.history.insert(
        0,
        {
            "time": datetime.now().strftime("%H:%M"),
            "level": level,
            "topic": topic,
            "difficulty": difficulty,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "correct": correct,
        },
    )


def difficulty_badge(difficulty: int) -> str:
    if difficulty == 1:
        label = "Kolay"
    elif difficulty == 2:
        label = "Orta"
    else:
        label = "Zor"
    return f'<span class="difficulty-badge difficulty-{difficulty}">Zorluk: {label}</span>'


def render_header():
    left, right = st.columns([3, 2])
    with left:
        st.markdown("### 🧠 Evde Matematik Asistanı")
        st.markdown(
            "_Akıllı yeni nesil sorular, anında geri bildirim ve detaylı çözüm adımları._"
        )
    with right:
        st.markdown(
            f"""
        <div style="text-align:right;">
            <span class="metric-label">TOPLAM PUAN</span><br>
            <span class="metric-number">{st.session_state.score}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🎯 Mod Seçimi")
        page_labels = ["Ana Sayfa", "Test Modu", "İstatistikler"]
        label_to_key = {"Ana Sayfa": "home", "Test Modu": "test", "İstatistikler": "stats"}
        key_to_label = {v: k for k, v in label_to_key.items()}

        current_label = key_to_label.get(st.session_state.page, "Ana Sayfa")
        selected_label = st.radio(
            "Sayfa",
            options=page_labels,
            index=page_labels.index(current_label),
        )
        st.session_state.page = label_to_key[selected_label]

        st.markdown("---")

        st.markdown("### 🧩 Öğrenme Seviyesi")
        level = st.selectbox(
            "Sınıf düzeyi",
            options=["4. Sınıf", "5. Sınıf"],
            index=0,
        )

        if level == "4. Sınıf":
            topic = st.selectbox(
                "Konu",
                options=[
                    "Toplama / Çıkarma",
                    "Çarpma / Bölme",
                    "Problem Çözme",
                ],
            )
        else:
            topic = st.selectbox(
                "Konu",
                options=[
                    "Doğal Sayılar / İşlemler",
                    "Oran / Orantı",
                    "Geometri (Çevre / Alan)",
                ],
            )

        st.markdown("---")

        total = st.session_state.total_questions
        correct = st.session_state.correct_answers
        accuracy = (correct / total * 100) if total > 0 else 0

        st.markdown("### 📈 Genel Durum")
        st.metric("Çözülen Soru", total)
        st.metric("Doğru Sayısı", correct)
        st.metric("Doğruluk Oranı", f"{accuracy:.0f}%")

        if st.button("🔄 Tüm İlerlemeyi Sıfırla"):
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.correct_answers = 0
            st.session_state.history = []
            reset_question()

        return level, topic


# --------------------
# SAYFA: ANA SAYFA
# --------------------
def render_home():
    render_header()
    st.markdown("")

    col1, col2, col3 = st.columns([1.2, 1.2, 1.2])

    with col1:
        st.markdown(
            """
        <div class="card">
            <div class="card-header">🎯 Odaklı Test</div>
            <div class="card-subtitle">
                Sınıf ve konu seç, seviyene uygun yeni nesil sorular çöz.
            </div>
            <span class="tag">Uyarlanabilir zorluk</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="card">
            <div class="card-header">🧩 Adım Adım Çözüm</div>
            <div class="card-subtitle">
                Yanlış yapsan bile, çözüm adımlarını görerek öğren.
            </div>
            <span class="tag">Anında geribildirim</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="card">
            <div class="card-header">📊 Veli Dostu İstatistik</div>
            <div class="card-subtitle">
                Doğruluk oranı, toplam puan ve tarihçeyi tek ekranda takip et.
            </div>
            <span class="tag">Güvenli ve reklamsız</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.info(
        "Uygulama, MEB kazanımlarına uygun şekilde tasarlanmış örnek sorular ve "
        "profesyonel bir arayüz sunar. Sol taraftan **Test Modu**'na geçip hemen dene."
    )

    with st.expander("🧪 Örnek Yeni Nesil Sorular (Önizleme)"):
        st.caption("Her yenilemede farklı örnekler gelir. Asıl çözme ekranı için sol menüden **Test Modu**'nu seç.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**4. Sınıf – Örnek**")
            q, a, _, d = generate_question("4. Sınıf", random.choice(["Toplama / Çıkarma", "Çarpma / Bölme", "Problem Çözme"]))
            st.write(q)
            st.caption(f"Zorluk: {d} · Cevap: {a}")
        with c2:
            st.markdown("**5. Sınıf – Örnek**")
            q, a, _, d = generate_question("5. Sınıf", random.choice(["Doğal Sayılar / İşlemler", "Oran / Orantı", "Geometri (Çevre / Alan)"]))
            st.write(q)
            st.caption(f"Zorluk: {d} · Cevap: {a}")


# --------------------
# SAYFA: TEST MODU
# --------------------
def render_test(level: str, topic: str):
    render_header()

    st.markdown("### 📝 Yeni Nesil Soru")

    if st.session_state.question_data is None:
        q, a, exp, diff = generate_question(level, topic)
        st.session_state.question_data = {
            "q": q,
            "a": a,
            "explanation": exp,
            "difficulty": diff,
            "level": level,
            "topic": topic,
        }

    qdata = st.session_state.question_data

    container = st.container()
    with container:
        st.markdown(
            f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
                <div>
                    <div class="card-header">❓ Soru</div>
                    <div class="card-subtitle">{qdata["level"]} · {qdata["topic"]}</div>
                </div>
                <div>
                    {difficulty_badge(qdata["difficulty"])}
                </div>
            </div>
            <div class="question-text">{qdata["q"].replace(chr(10), "<br>")}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    answer_col, meta_col = st.columns([2, 1])

    with answer_col:
        user_answer = st.number_input(
            "Cevabını buraya yaz",
            step=1,
            format="%d",
        )

        check_clicked = st.button("✅ Cevabı Kontrol Et", type="primary", use_container_width=True)

        if check_clicked:
            correct = user_answer == qdata["a"]
            record_result(
                correct=correct,
                user_answer=user_answer,
                correct_answer=qdata["a"],
                level=qdata["level"],
                topic=qdata["topic"],
                difficulty=qdata["difficulty"],
            )

            if correct:
                st.success("🎉 Harika! Doğru cevap verdin.")
            else:
                st.error(
                    f"❌ Bu kez olmadı. Doğru cevap: **{qdata['a']}**\n\n"
                    "Aşağıdan çözüm adımlarını inceleyebilirsin."
                )

            with st.expander("📚 Adım Adım Çözümü Gör"):
                st.markdown(qdata["explanation"].replace("\n", "  \n"))

            next_col1, next_col2 = st.columns([1, 1])
            with next_col1:
                if st.button("🆕 Yeni Soru", use_container_width=True):
                    reset_question()
                    st.rerun()
            with next_col2:
                if st.button("🏠 Ana Sayfa", use_container_width=True):
                    reset_question()
                    st.session_state.page = "home"
                    st.rerun()

    with meta_col:
        st.markdown("#### 📌 Bilgiler")
        st.write(f"- Sınıf: **{qdata['level']}**")
        st.write(f"- Konu: **{qdata['topic']}**")
        st.write(f"- Doğru Cevap: **{qdata['a']}**")
        st.write(f"- Kazanılacak Puan: **{10 * qdata['difficulty']}**")


# --------------------
# SAYFA: İSTATİSTİKLER
# --------------------
def render_stats():
    render_header()
    st.markdown("### 📊 Öğrenci İstatistikleri")

    total = st.session_state.total_questions
    correct = st.session_state.correct_answers
    accuracy = (correct / total * 100) if total > 0 else 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
        <div class="card" style="text-align:center;">
            <div class="metric-label">ÇÖZÜLEN SORU</div>
            <div class="metric-number">{total}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
        <div class="card" style="text-align:center;">
            <div class="metric-label">DOĞRU SAYISI</div>
            <div class="metric-number">{correct}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
        <div class="card" style="text-align:center;">
            <div class="metric-label">DOĞRULUK ORANI</div>
            <div class="metric-number">{accuracy:.0f}%</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
        <div class="card" style="text-align:center;">
            <div class="metric-label">TOPLAM PUAN</div>
            <div class="metric-number">{st.session_state.score}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("#### 🕘 Son Çözülen Sorular")

    if not st.session_state.history:
        st.info("Henüz çözülmüş soru bulunmuyor. Sol menüden **Test Modu**'na geçebilirsin.")
        return

    for item in st.session_state.history[:10]:
        icon = "✅" if item["correct"] else "❌"
        color = "#22c55e" if item["correct"] else "#ef4444"
        st.markdown(
            f"""
        <div class="card" style="margin-bottom:0.5rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-weight:600;">{icon} {item["level"]} - {item["topic"]}</span><br>
                    <span style="font-size:0.8rem;color:#6b7280;">
                        Senin cevabın: <b>{item["user_answer"]}</b> · Doğru cevap: <b>{item["correct_answer"]}</b>
                    </span>
                </div>
                <div style="text-align:right;">
                    <span style="font-size:0.8rem;color:#9ca3af;">{item["time"]}</span><br>
                    <span style="font-size:0.8rem;color:{color};">
                        {"Doğru" if item["correct"] else "Yanlış"}
                    </span>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


# --------------------
# ANA UYGULAMA AKIŞI
# --------------------
def main():
    level, topic = render_sidebar()

    # İçerik alanı
    page_key = st.session_state.page
    if page_key == "home":
        render_home()
    elif page_key == "test":
        render_test(level, topic)
    elif page_key == "stats":
        render_stats()
    else:
        st.session_state.page = "home"
        st.rerun()

    st.markdown(
        '<div class="footer-text">© '
        + str(datetime.now().year)
        + ' Evde Matematik Asistanı · Geliştirilmiş eğitim arayüzü</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()


