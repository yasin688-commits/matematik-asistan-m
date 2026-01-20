import random
import io
import hashlib
from datetime import datetime

import streamlit as st
from PIL import Image, ImageDraw, ImageFont

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

if "subject_stats" not in st.session_state:
    # subject -> {"total": int, "correct": int}
    st.session_state.subject_stats = {}

if "seen_correct" not in st.session_state:
    # Doğru yapılan sorular tekrar sorulmaz (id set)
    st.session_state.seen_correct = set()


# --------------------
# SORU ÜRETİCİLER
# --------------------
def _font(size: int = 18) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arial.ttf", size=size)
    except Exception:
        return ImageFont.load_default()


def _img_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _card_image(title: str, lines: list[str], w: int = 900, h: int = 420) -> bytes:
    img = Image.new("RGB", (w, h), (250, 252, 255))
    draw = ImageDraw.Draw(img)

    # header bar
    draw.rounded_rectangle([20, 20, w - 20, 88], radius=18, fill=(233, 243, 255), outline=(210, 225, 245))
    draw.text((40, 38), title, fill=(15, 23, 42), font=_font(22))

    # body card
    draw.rounded_rectangle([20, 110, w - 20, h - 20], radius=18, fill=(255, 255, 255), outline=(220, 230, 242))

    y = 140
    for line in lines:
        draw.text((40, y), line, fill=(17, 24, 39), font=_font(18))
        y += 32

    return _img_bytes(img)


def _bar_chart_image(labels: list[str], values: list[int], title: str) -> bytes:
    w, h = 900, 420
    img = Image.new("RGB", (w, h), (250, 252, 255))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([20, 20, w - 20, h - 20], radius=18, fill=(255, 255, 255), outline=(220, 230, 242))
    draw.text((40, 32), title, fill=(15, 23, 42), font=_font(22))

    max_v = max(values) if values else 1
    chart_left, chart_top, chart_right, chart_bottom = 60, 90, w - 60, h - 80
    draw.line([chart_left, chart_bottom, chart_right, chart_bottom], fill=(148, 163, 184), width=2)
    draw.line([chart_left, chart_top, chart_left, chart_bottom], fill=(148, 163, 184), width=2)

    bar_w = int((chart_right - chart_left) / max(1, len(values)) * 0.6)
    gap = int((chart_right - chart_left) / max(1, len(values)) * 0.4)

    x = chart_left + gap // 2
    for lab, v in zip(labels, values):
        bar_h = int((chart_bottom - chart_top) * (v / max_v))
        x1, y1 = x, chart_bottom - bar_h
        x2, y2 = x + bar_w, chart_bottom
        draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=(99, 102, 241), outline=(79, 70, 229))
        draw.text((x1, chart_bottom + 8), lab, fill=(55, 65, 81), font=_font(16))
        draw.text((x1, y1 - 22), str(v), fill=(55, 65, 81), font=_font(16))
        x += bar_w + gap

    return _img_bytes(img)


def _timeline_image(events: list[tuple[str, str]], title: str) -> bytes:
    w, h = 900, 420
    img = Image.new("RGB", (w, h), (250, 252, 255))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([20, 20, w - 20, h - 20], radius=18, fill=(255, 255, 255), outline=(220, 230, 242))
    draw.text((40, 32), title, fill=(15, 23, 42), font=_font(22))

    line_y = 220
    draw.line([80, line_y, w - 80, line_y], fill=(148, 163, 184), width=4)

    n = max(1, len(events))
    step = int((w - 160) / n)
    x = 80 + step // 2
    for i, (year, label) in enumerate(events):
        draw.ellipse([x - 10, line_y - 10, x + 10, line_y + 10], fill=(16, 185, 129))
        draw.text((x - 22, line_y - 44), year, fill=(15, 23, 42), font=_font(16))
        draw.text((x - 80, line_y + 20), label, fill=(55, 65, 81), font=_font(16))
        x += step

    return _img_bytes(img)


def _mini_map_image(points: dict[str, tuple[int, int]], title: str) -> bytes:
    w, h = 900, 420
    img = Image.new("RGB", (w, h), (250, 252, 255))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([20, 20, w - 20, h - 20], radius=18, fill=(255, 255, 255), outline=(220, 230, 242))
    draw.text((40, 32), title, fill=(15, 23, 42), font=_font(22))

    # map area
    mx1, my1, mx2, my2 = 60, 90, w - 60, h - 60
    draw.rounded_rectangle([mx1, my1, mx2, my2], radius=18, fill=(236, 253, 245), outline=(167, 243, 208))
    # simple "sea" band
    draw.rounded_rectangle([mx1, my2 - 70, mx2, my2], radius=18, fill=(219, 234, 254), outline=(191, 219, 254))
    draw.text((mx1 + 16, my2 - 55), "DENİZ", fill=(30, 64, 175), font=_font(16))

    for name, (x, y) in points.items():
        px = mx1 + x
        py = my1 + y
        draw.ellipse([px - 10, py - 10, px + 10, py + 10], fill=(239, 68, 68))
        draw.text((px + 14, py - 12), name, fill=(15, 23, 42), font=_font(18))

    return _img_bytes(img)


def _normalize_text(s: str) -> str:
    return (s or "").strip().casefold()

def _question_id(subject: str, level: str, topic: str, q: str, a) -> str:
    base = f"{subject}|{level}|{topic}|{q}|{a}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]


def _make_numeric_choices(answer: int, k: int = 4) -> list[int]:
    """Doğru cevaptan mantıklı sayısal çeldiriciler üretir (şık)."""
    answer = int(answer)
    choices = {answer}

    # Farklı tipte çeldiriciler
    deltas = [1, 2, 3, 4, 5, 8, 10, 12, 15, 20, 25, 30]
    random.shuffle(deltas)

    for d in deltas:
        if len(choices) >= k:
            break
        for cand in (answer + d, answer - d):
            if cand >= 0:
                choices.add(cand)
            if len(choices) >= k:
                break

    # Bazı oransal çeldiriciler (uygun olursa)
    for cand in (answer * 2, max(0, answer // 2), answer + 50, max(0, answer - 50)):
        if len(choices) >= k:
            break
        choices.add(int(cand))

    # Hâlâ yetmiyorsa rastgele doldur
    while len(choices) < k:
        jitter = random.randint(1, 40)
        cand = max(0, answer + random.choice([-1, 1]) * jitter)
        choices.add(cand)

    out = list(choices)[:k]
    random.shuffle(out)
    return out


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
# DERS BAZLI (GÖRSEL ODAKLI) SORULAR
# --------------------
def generate_turkce_question(level: str):
    # Görsel: cümlede altı çizili kelime, doğru yazımı seç
    variants = [
        ("yanlız", "yalnız"),
        ("herkez", "herkes"),
        ("şöför", "şoför"),
        ("deyil", "değil"),
        ("fasülye", "fasulye"),
    ]
    wrong, correct = random.choice(variants)
    sentence = f"Bugün {wrong} okula gitti."
    img = _card_image(
        "Türkçe: Yazım Yanlışı",
        [
            "Aşağıdaki cümlede yazım yanlışı yapılmıştır.",
            "",
            sentence,
            "",
            "Soru: Yanlış yazılan kelimenin doğru yazımı hangisidir?",
        ],
    )
    choices = [correct, wrong, correct.replace("ı", "i"), correct + " "]
    choices = list(dict.fromkeys([c.strip() for c in choices]))[:4]
    random.shuffle(choices)
    return {
        "q": "Görseldeki cümlede yanlış yazılan kelimenin doğru yazımı hangisidir?",
        "type": "choice",
        "choices": choices,
        "a": correct,
        "explanation": f"Doğru yazım: **{correct}**",
        "difficulty": 2,
        "image": img,
        "subject": "Türkçe",
        "topic": "Yazım Kuralları",
        "level": level,
    }


def generate_fen_question(level: str):
    # Görsel: besin zinciri şeması -> eksik halkayı seç
    chain = [
        ("Bitki", "Çekirge", "Kurbağa", "Yılan"),
        ("Ot", "Tavşan", "Tilki", "Kartal"),
    ]
    a, b, c, d = random.choice(chain)
    missing = random.choice([b, c])
    shown = [a, "____", c, d] if missing == b else [a, b, "____", d]
    img = _card_image(
        "Fen Bilimleri: Besin Zinciri",
        [
            "Aşağıdaki besin zincirinde bir canlı eksiktir.",
            "",
            "  →  ".join(shown),
            "",
            "Soru: Boş bırakılan yere hangisi gelmelidir?",
        ],
    )
    choices = [b, c, d, a]
    choices = list(dict.fromkeys(choices))
    random.shuffle(choices)
    return {
        "q": "Besin zincirinde boş bırakılan yere hangisi gelmelidir?",
        "type": "choice",
        "choices": choices,
        "a": missing,
        "explanation": f"Doğru zincir: {a} → {b} → {c} → {d}",
        "difficulty": 2,
        "image": img,
        "subject": "Fen Bilimleri",
        "topic": "Besin Zinciri",
        "level": level,
    }


def generate_sosyal_question(level: str):
    # Görsel: sütun grafiği (nüfus/üretim vb.) -> en büyük / fark
    cities = ["A", "B", "C", "D"]
    values = [random.randint(20, 80) for _ in cities]
    img = _bar_chart_image(cities, values, "Sosyal: Sütun Grafiği (Örnek Veri)")
    idx = values.index(max(values))
    answer = cities[idx]
    return {
        "q": "Grafiğe göre değeri en yüksek olan şehir hangisidir?",
        "type": "choice",
        "choices": cities,
        "a": answer,
        "explanation": f"En yüksek değer {max(values)} ile **{answer}** şehrindedir.",
        "difficulty": 2,
        "image": img,
        "subject": "Sosyal Bilgiler",
        "topic": "Grafik Okuma",
        "level": level,
    }


def generate_english_question(level: str):
    # Görsel: kelime kartı (renk/nesne) -> doğru İngilizce kelimeyi seç
    items = [
        ("apple", "Elma"),
        ("book", "Kitap"),
        ("chair", "Sandalye"),
        ("water", "Su"),
        ("school", "Okul"),
    ]
    en, tr = random.choice(items)
    img = _card_image(
        "English: Word Card",
        [
            "Look at the card and choose the correct meaning.",
            "",
            f"WORD: {en.upper()}",
            "",
            "Question: What is the Turkish meaning?",
        ],
    )
    distractors = [t for _, t in items if t != tr]
    choices = random.sample(distractors, k=3) + [tr]
    random.shuffle(choices)
    return {
        "q": f"'{en}' kelimesinin Türkçe anlamı hangisidir?",
        "type": "choice",
        "choices": choices,
        "a": tr,
        "explanation": f"'{en}' = **{tr}**",
        "difficulty": 1,
        "image": img,
        "subject": "İngilizce",
        "topic": "Kelime",
        "level": level,
    }


def generate_tarih_question(level: str):
    # Görsel: zaman çizgisi -> sıralama / hangisi önce
    events = [
        ("1920", "TBMM"),
        ("1923", "Cumhuriyet"),
        ("1938", "Atatürk"),
        ("1919", "Samsun"),
    ]
    chosen = random.sample(events, k=3)
    # sort by year for timeline
    chosen_sorted = sorted(chosen, key=lambda x: int(x[0]))
    img = _timeline_image(chosen_sorted, "Tarih: Zaman Çizgisi (Örnek)")
    # ask earliest event
    answer = chosen_sorted[0][1]
    choices = [e[1] for e in chosen_sorted]
    random.shuffle(choices)
    return {
        "q": "Zaman çizgisine göre en önce gerçekleşen olay hangisidir?",
        "type": "choice",
        "choices": choices,
        "a": answer,
        "explanation": f"En erken yıl {chosen_sorted[0][0]} olduğundan cevap **{answer}**.",
        "difficulty": 2,
        "image": img,
        "subject": "Tarih",
        "topic": "Zaman Çizgisi",
        "level": level,
    }


def generate_cografya_question(level: str):
    # Görsel: mini harita -> yön bulma
    points = {
        "K": (180, 80),   # Kuzey
        "G": (220, 220),  # Güney
        "D": (520, 150),  # Doğu
        "B": (80, 160),   # Batı
    }
    # choose two points, ask relative direction
    names = list(points.keys())
    src, dst = random.sample(names, k=2)
    img = _mini_map_image({src: points[src], dst: points[dst]}, "Coğrafya: Yön Bulma (Mini Harita)")

    dx = points[dst][0] - points[src][0]
    dy = points[dst][1] - points[src][1]
    horiz = "doğusunda" if dx > 0 else "batısında"
    vert = "güneyinde" if dy > 0 else "kuzeyinde"
    # pick dominant direction for simple question
    answer = horiz if abs(dx) >= abs(dy) else vert
    choices = ["kuzeyinde", "güneyinde", "doğusunda", "batısında"]
    return {
        "q": f"Haritaya göre **{dst}**, **{src}** noktasının daha çok hangisindedir?",
        "type": "choice",
        "choices": choices,
        "a": answer,
        "explanation": f"Konuma göre **{dst}**, **{src}** noktasının {answer}.",
        "difficulty": 2,
        "image": img,
        "subject": "Coğrafya",
        "topic": "Yönler",
        "level": level,
    }


def generate_subject_question(subject: str, level: str):
    if subject == "Matematik":
        # Matematik mevcut üreticiyi kullanıyor (görselsiz/karışık). İleride görselleştirilebilir.
        # Bu fonksiyon matematiği çağıran yerde topic ile üretilecek.
        raise ValueError("Matematik için topic gerekli.")
    if subject == "Türkçe":
        return generate_turkce_question(level)
    if subject == "Fen Bilimleri":
        return generate_fen_question(level)
    if subject == "Sosyal Bilgiler":
        return generate_sosyal_question(level)
    if subject == "İngilizce":
        return generate_english_question(level)
    if subject == "Tarih":
        return generate_tarih_question(level)
    if subject == "Coğrafya":
        return generate_cografya_question(level)
    return generate_turkce_question(level)


# --------------------
# YARDIMCI FONKSİYONLAR
# --------------------
def reset_question():
    st.session_state.question_data = None


def record_result(correct: bool, user_answer, correct_answer, level, subject, topic, difficulty):
    st.session_state.total_questions += 1
    if correct:
        st.session_state.correct_answers += 1
        st.session_state.score += 10 * difficulty

    if subject not in st.session_state.subject_stats:
        st.session_state.subject_stats[subject] = {"total": 0, "correct": 0}
    st.session_state.subject_stats[subject]["total"] += 1
    if correct:
        st.session_state.subject_stats[subject]["correct"] += 1

    st.session_state.history.insert(
        0,
        {
            "time": datetime.now().strftime("%H:%M"),
            "level": level,
            "subject": subject,
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

        st.markdown("### 📚 Ders Seçimi")
        subject = st.selectbox(
            "Ders",
            options=[
                "Matematik",
                "Türkçe",
                "Fen Bilimleri",
                "Sosyal Bilgiler",
                "İngilizce",
                "Tarih",
                "Coğrafya",
            ],
            index=0,
        )

        st.markdown("---")

        st.markdown("### 🧩 Öğrenme Seviyesi")
        level = st.selectbox(
            "Sınıf düzeyi",
            options=["4. Sınıf", "5. Sınıf"],
            index=0,
        )

        topic = None
        if subject == "Matematik":
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
        else:
            st.caption("Bu derste sorular **görsel odaklı** ve genelde **çoktan seçmeli** gelir.")

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
            st.session_state.subject_stats = {}
            reset_question()

        return subject, level, topic


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
def render_test(subject: str, level: str, topic: str | None):
    render_header()

    st.markdown("### 📝 Yeni Nesil Soru")

    if st.session_state.question_data is None:
        if subject == "Matematik":
            q, a, exp, diff = generate_question(level, topic or "Toplama / Çıkarma")
            st.session_state.question_data = {
                "q": q,
                "a": a,
                "explanation": exp,
                "difficulty": diff,
                "level": level,
                "topic": topic or "Toplama / Çıkarma",
                "subject": "Matematik",
                "type": "choice",
                "choices": _make_numeric_choices(a, k=4),
                "image": None,
            }
        else:
            st.session_state.question_data = generate_subject_question(subject, level)

    qdata = st.session_state.question_data

    container = st.container()
    with container:
        st.markdown(
            f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
                <div>
                    <div class="card-header">❓ Soru</div>
                    <div class="card-subtitle">{qdata.get("subject","")} · {qdata["level"]} · {qdata["topic"]}</div>
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
        if qdata.get("image"):
            st.image(qdata["image"], use_container_width=True)

        qtype = qdata.get("type", "number")
        if qtype == "choice":
            user_answer = st.radio(
                "Seçeneğini işaretle",
                options=qdata.get("choices", []),
                index=None,
                horizontal=False,
            )
        elif qtype == "text":
            user_answer = st.text_input("Cevabını yaz")
        else:
            user_answer = st.number_input(
                "Cevabını buraya yaz",
                step=1,
                format="%d",
            )

        check_clicked = st.button("✅ Cevabı Kontrol Et", type="primary", use_container_width=True)

        if check_clicked:
            if qtype == "choice":
                correct = user_answer == qdata["a"]
            elif qtype == "text":
                correct = _normalize_text(user_answer) == _normalize_text(str(qdata["a"]))
            else:
                correct = user_answer == qdata["a"]
            record_result(
                correct=correct,
                user_answer=user_answer,
                correct_answer=qdata["a"],
                level=qdata["level"],
                subject=qdata.get("subject", subject),
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
        st.write(f"- Ders: **{qdata.get('subject', subject)}**")
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

    st.markdown("#### 📚 Ders Bazlı Durum")
    if st.session_state.subject_stats:
        cols = st.columns(min(4, len(st.session_state.subject_stats)))
        i = 0
        for subj, stats in st.session_state.subject_stats.items():
            total_s = stats.get("total", 0)
            correct_s = stats.get("correct", 0)
            acc_s = (correct_s / total_s * 100) if total_s else 0
            with cols[i % len(cols)]:
                st.markdown(
                    f"""
                <div class="card" style="text-align:center;margin-bottom:0.5rem;">
                    <div class="metric-label">{subj}</div>
                    <div class="metric-number">{acc_s:.0f}%</div>
                    <div style="color:#6b7280;font-size:0.85rem;">{correct_s}/{total_s} doğru</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            i += 1
    else:
        st.caption("Ders bazlı istatistik için önce soru çöz.")

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
                    <span style="font-weight:600;">{icon} {item.get("subject","")} · {item["level"]} - {item["topic"]}</span><br>
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
    subject, level, topic = render_sidebar()

    # İçerik alanı
    page_key = st.session_state.page
    if page_key == "home":
        render_home()
    elif page_key == "test":
        render_test(subject, level, topic)
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


