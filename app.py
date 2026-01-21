import streamlit as st
import random

# 1. SAYFA AYARLARI VE TASARIM
st.set_page_config(page_title="5. Sınıf Eğitim Portalı", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #001C30; }
    .quiz-header { display: flex; justify-content: space-around; align-items: center; background-color: #1a3a5a; padding: 12px; border-radius: 12px; color: white; margin-bottom: 15px; }
    .score-badge { padding: 5px 15px; border-radius: 20px; font-weight: bold; min-width: 40px; text-align: center; }
    .correct-bg { background-color: #4CAF50; }
    .wrong-bg { background-color: #F44336; }
    .question-box { background-color: white; color: black; padding: 25px; border-radius: 10px; font-size: 18px; line-height: 1.6; border-left: 8px solid #2196F3; margin-bottom: 15px; }
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    .test-card { background-color: #8BC34A; border-radius: 20px; padding: 15px; margin-bottom: 10px; color: #102A43; }
    .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; justify-content: space-around; padding: 10px; z-index: 1000; border-top: 1px solid #ccc; }
    </style>
    """, unsafe_allow_html=True)

# 2. GERÇEK ŞIKLI SORU ÜRETİCİSİ
def soru_getir(ders, unite, soru_no):
    # Her soru için sabit ama benzersiz veriler üretir
    seed_val = f"{ders}_{unite}_{soru_no}"
    random.seed(seed_val)
    
    # Örnek Soru Bankası
    if ders == "Matematik":
        s1 = random.randint(100, 500)
        s2 = random.randint(50, 100)
        dogru = s1 + s2
        yanlislar = [dogru-10, dogru+10, dogru+5]
        soru_metni = f"<b>{s1} + {s2}</b> işleminin sonucu aşağıdakilerden hangisidir?"
        secenekler = [str(dogru), str(yanlislar[0]), str(yanlislar[1]), str(yanlislar[2])]
    elif ders == "Fen Bilimleri":
        soru_metni = "Güneş ile ilgili hangisi uygun bir yöntem <u>değildir</u>?"
        secenekler = ["Teleskopla bakmak", "Doğrudan büyüteçle bakmak", "Uydu görüntüleri", "Filtreli gözlük"]
        dogru = secenekler[1]
    else:
        soru_metni = f"{ders} dersi {unite} ünitesi üzerine bir mantık sorusudur."
        secenekler = ["Seçenek A", "Seçenek B", "Seçenek C", "Seçenek D"]
        dogru = secenekler[0]

    random.shuffle(secenekler) # Şıkların yerini karıştır
    return {
        "soru": soru_metni,
        "A": secenekler[0], "B": secenekler[1], "C": secenekler[2], "D": secenekler[3],
        "dogru": secenekler.index(dogru) # 0, 1, 2, 3 olarak index tutar
    }

# 3. OTURUM DURUMU
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'stats' not in st.session_state: st.session_state.stats = {}
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
if 'cevaplandi' not in st.session_state: st.session_state.cevaplandi = False

def navigate(to):
    st.session_state.page = to
    st.session_state.cevaplandi = False
    st.rerun()

# 4. SAYFALAR

# --- ANA SAYFA ---
if st.session_state.page == 'home':
    st.markdown('<h2 style="color:white; text-align:center;">5. Sınıf Test Paneli</h2>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📝\nTestler"): navigate('kategoriler')
        st.button("🎬\nVideolar")
    with c2:
        st.button("❓\nRastgele")
        st.button("❤️\nFavori")
    with c3:
        st.button("📊\nİstatistik")
        st.button("❌\nKapat")

# --- KATEGORİLER ---
elif st.session_state.page == 'kategoriler':
    st.markdown('<h3 style="color:white;">Ders Seçiniz</h3>', unsafe_allow_html=True)
    dersler = ["Matematik", "Türkçe", "Fen Bilimleri", "Sosyal Bilgiler", "İngilizce", "Din Kültürü"]
    for d in dersler:
        if st.button(f"📚 {d} \n ✓ Kategori"):
            st.session_state.active_ders = d
            navigate('test_listesi')

# --- TEST LİSTESİ ---
elif st.session_state.page == 'test_listesi':
    ders = st.session_state.active_ders
    st.markdown(f'<h3 style="color:white;">{ders} Üniteleri</h3>', unsafe_allow_html=True)
    uniteler = ["1. Ünite", "2. Ünite", "3. Ünite"]
    for u in uniteler:
        t_key = f"{ders}_{u}"
        s = st.session_state.stats.get(t_key, {"d":0, "y":0})
        st.markdown(f'<div class="test-card">📋 {u} - Doğru: {s["d"]} | Yanlış: {s["y"]}</div>', unsafe_allow_html=True)
        if st.button(f"Testi Başlat: {u}", key=u):
            st.session_state.active_unite = u
            st.session_state.q_idx = 0
            navigate('quiz')

# --- SORU EKRANI ---
elif st.session_state.page == 'quiz':
    ders = st.session_state.active_ders
    unite = st.session_state.active_unite
    idx = st.session_state.q_idx
    t_key = f"{ders}_{unite}"
    
    if t_key not in st.session_state.stats: st.session_state.stats[t_key] = {"d": 0, "y": 0}
    
    soru_data = soru_getir(ders, unite, idx + 1)
    harfler = ["A", "B", "C", "D"]
    
    # Üst Panel
    st.markdown(f"""
        <div class="quiz-header">
            <span>⏰ 02:30</span>
            <span style="font-weight:bold;">{idx + 1} / 20</span>
            <span class="score-badge wrong-bg">{st.session_state.stats[t_key]['y']}</span>
            <span class="score-badge correct-bg">{st.session_state.stats[t_key]['d']}</span>
            <span>📝</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="question-box">{soru_data["soru"]}</div>', unsafe_allow_html=True)

    # Gerçek Şıklar
    for i, h in enumerate(harfler):
        if st.button(f"{h}) {soru_data[h]}", key=f"q_{idx}_{h}"):
            if not st.session_state.cevaplandi:
                if i == soru_data["dogru"]:
                    st.session_state.stats[t_key]["d"] += 1
                    st.success("Doğru!")
                else:
                    st.session_state.stats[t_key]["y"] += 1
                    dogru_harf = harfler[soru_data["dogru"]]
                    st.error(f"Yanlış! Doğru Cevap: {dogru_harf}")
                st.session_state.cevaplandi = True

    # Navigasyon
    st.write("---")
    nc1, nc2, nc3, nc4 = st.columns(4)
    with nc1:
        if st.button("⬅️ Geri"):
            if st.session_state.q_idx > 0:
                st.session_state.q_idx -= 1
                st.session_state.cevaplandi = False
                st.rerun()
    with nc2: st.button("❤️")
    with nc3:
        if st.button("İleri ➡️"):
            if st.session_state.q_idx < 19:
                st.session_state.q_idx += 1
                st.session_state.cevaplandi = False
                st.rerun()
            else: st.balloons(); navigate('test_listesi')
    with nc4:
        if st.button("❌"): navigate('test_listesi')

# 5. ALT İKONLAR
st.write("<br><br><br>", unsafe_allow_html=True)
cols = st.columns(5)
with cols[0]:
    if st.button("🏠"): navigate('home')
with cols[1]:
    if st.button("📋"): navigate('kategoriler')
with cols[2]: st.button("📊")
with cols[3]: st.button("❤️")
with cols[4]:
    if st.button("◀️"): navigate('kategoriler')
