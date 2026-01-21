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
    </style>
    """, unsafe_allow_html=True)

# 2. HATA VERMEYEN SORU ÜRETİCİSİ
def soru_getir(ders, unite, soru_no):
    # Tohumlama yaparak her sorunun her seferinde aynı gelmesini sağlıyoruz
    random.seed(f"{ders}_{unite}_{soru_no}")
    
    if ders == "Fen Bilimleri":
        soru_metni = "Güneş ile ilgili hangisi uygun bir yöntem değildir?"
        dogru_cevap = "Doğrudan büyüteçle bakmak"
        yanlislar = ["Filtreli teleskop kullanmak", "Uydu görüntülerini incelemek", "Özel güneş gözlüğü kullanmak"]
    elif ders == "Matematik":
        s1 = random.randint(100, 500)
        s2 = random.randint(50, 100)
        soru_metni = f"<b>{s1} + {s2}</b> işleminin sonucu kaçtır?"
        dogru_cevap = str(s1 + s2)
        yanlislar = [str(s1 + s2 + 10), str(s1 + s2 - 5), str(s1 + s2 + 2)]
    else:
        soru_metni = f"{ders} {unite} Soru {soru_no}: Bu konu hakkında hangisi doğrudur?"
        dogru_cevap = "Doğru Seçenek"
        yanlislar = ["Yanlış A", "Yanlış B", "Yanlış C"]

    # Şıkları birleştir ve karıştır
    secenekler = yanlislar + [dogru_cevap]
    random.shuffle(secenekler)
    
    return {
        "soru": soru_metni,
        "A": secenekler[0], "B": secenekler[1], "C": secenekler[2], "D": secenekler[3],
        "dogru_icerik": dogru_cevap # Index yerine içerik kontrolü yaparak hatayı önlüyoruz
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
    st.markdown('<h2 style="color:white; text-align:center;">5. Sınıf Eğitim Paneli</h2>', unsafe_allow_html=True)
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
    if st.button("⬅️ Geri"): navigate('home')

# --- TEST LİSTESİ ---
elif st.session_state.page == 'test_listesi':
    ders = st.session_state.active_ders
    st.markdown(f'<h3 style="color:white;">{ders} Üniteleri</h3>', unsafe_allow_html=True)
    for i in range(1, 4):
        unite = f"{i}. Ünite"
        t_key = f"{ders}_{unite}"
        s = st.session_state.stats.get(t_key, {"d":0, "y":0})
        st.markdown(f'<div class="test-card">📋 {unite} - Doğru: {s["d"]} | Yanlış: {s["y"]}</div>', unsafe_allow_html=True)
        if st.button(f"Başlat: {unite}", key=t_key):
            st.session_state.active_unite = unite
            st.session_state.q_idx = 0
            navigate('quiz')
    if st.button("⬅️ Geri"): navigate('kategoriler')

# --- SORU EKRANI ---
elif st.session_state.page == 'quiz':
    ders = st.session_state.active_ders
    unite = st.session_state.active_unite
    idx = st.session_state.q_idx
    t_key = f"{ders}_{unite}"
    
    if t_key not in st.session_state.stats: st.session_state.stats[t_key] = {"d": 0, "y": 0}
    
    soru_data = soru_getir(ders, unite, idx + 1)
    
    # Üst Bilgi
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

    # Şıklar
    for h in ["A", "B", "C", "D"]:
        secenek_metni = soru_data[h]
        if st.button(f"{h}) {secenek_metni}", key=f"q_{idx}_{h}"):
            if not st.session_state.cevaplandi:
                if secenek_metni == soru_data["dogru_icerik"]:
                    st.session_state.stats[t_key]["d"] += 1
                    st.success("DOĞRU!")
                else:
                    st.session_state.stats[t_key]["y"] += 1
                    st.error(f"YANLIŞ! Doğru Cevap: {soru_data['dogru_icerik']}")
                st.session_state.cevaplandi = True

    # Navigasyon Butonları
    st.write("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("⬅️ Geri"):
            if st.session_state.q_idx > 0:
                st.session_state.q_idx -= 1
                st.session_state.cevaplandi = False
                st.rerun()
    with c2: st.button("❤️")
    with c3:
        if st.button("İleri ➡️"):
            if st.session_state.q_idx < 19:
                st.session_state.q_idx += 1
                st.session_state.cevaplandi = False
                st.rerun()
            else: navigate('test_listesi')
    with c4:
        if st.button("❌"): navigate('test_listesi')

# SABİT ALT MENÜ
st.write("<br><br>", unsafe_allow_html=True)
b_cols = st.columns(5)
with b_cols[0]:
    if st.button("🏠"): navigate('home')
with b_cols[1]:
    if st.button("📋"): navigate('kategoriler')
with b_cols[2]: st.button("📊")
with b_cols[3]: st.button("❤️")
with b_cols[4]:
    if st.button("◀️"): navigate('kategoriler')
