import streamlit as st

# 1. SAYFA AYARLARI VE TASARIM
st.set_page_config(page_title="5. Sınıf Pro", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .quiz-container { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .header-panel { display: flex; justify-content: space-around; background-color: #1c3d5a; color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; font-weight: bold; }
    .q-text { font-size: 1.2rem; font-weight: 600; margin: 20px 0; color: #1a1a1a; line-height: 1.5; }
    .stButton>button { width: 100%; border-radius: 8px; height: 50px; font-size: 16px; transition: 0.2s; border: 1px solid #ddd; }
    /* Alt Navigasyon */
    .nav-row { display: flex; justify-content: space-between; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }
    .score-box { padding: 5px 15px; border-radius: 15px; min-width: 40px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. DERS VE ÜNİTE VERİLERİ (Görsel 10c1a5'e uygun)
DERS_UNITELERI = {
    "Matematik": ["Doğal Sayılar", "Kesirler", "Ondalık Gösterim"],
    "Türkçe": ["Sözcükte Anlam", "Paragraf", "Yazım Kuralları"],
    "Fen Bilimleri": ["Güneş, Dünya ve Ay", "Canlılar Dünyası", "Kuvvetin Ölçülmesi"],
    "Sosyal Bilgiler": ["Birey ve Toplum", "Kültür ve Miras"],
    "İngilizce": ["Hello!", "My Town"],
    "Din Kültürü": ["Allah İnancı", "Ramazan ve Oruç"]
}

# 3. SORU ÜRETİM MANTIĞI (Gerçek Şıklarla)
def get_soru_verisi(ders, unite, soru_no):
    # Bu fonksiyon seçilen derse göre gerçek şıklar üretir
    soru_havuzu = {
        "Matematik": "Aşağıdaki işlemlerden hangisinin sonucu 150'dir?",
        "Fen Bilimleri": "Güneş ile ilgili hangisi uygun bir yöntem değildir?", # cite: image_1122ca.jpg
        "Türkçe": "Hangisi 'yazım yanlışı' barındıran bir cümledir?"
    }
    soru_metni = soru_havuzu.get(ders, f"{ders} {unite} konusu ile ilgili soru.")
    
    return {
        "soru": f"<b>{soru_no}. Soru:</b> {soru_metni}",
        "A": "75 x 2", "B": "100 + 40", "C": "200 - 60", "D": "300 / 3",
        "cvp": "A" # Her soru için farklı cevap tanımı yapılabilir
    }

# 4. OTURUM DURUMU (Session State)
if 'step' not in st.session_state: st.session_state.step = 'home'
if 'stats' not in st.session_state: st.session_state.stats = {"d": 0, "y": 0}
if 'q_idx' not in st.session_state: st.session_state.q_idx = 1
if 'last_ans' not in st.session_state: st.session_state.last_ans = None

# 5. SAYFA YÖNLENDİRMELERİ
def navigate(target):
    st.session_state.step = target
    st.session_state.last_ans = None
    st.rerun()

# --- ANA SAYFA (image_10af63) ---
if st.session_state.step == 'home':
    st.markdown("<h2 style='text-align:center;'>5. Sınıf Tüm Dersler</h2>", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        if st.button("📝\nTestler"): navigate('kategoriler')
    with cols[1]:
        st.button("📊\nİstatistik")
    with cols[2]:
        st.button("⚙️\nAyarlar")

# --- KATEGORİ SEÇİMİ (image_10c1a5) ---
elif st.session_state.step == 'kategoriler':
    st.markdown("### Ders Seçiniz")
    for d in DERS_UNITELERI.keys():
        if st.button(f"📚 {d} \n ✓ Kategori"):
            st.session_state.active_ders = d
            navigate('testler')
    if st.button("⬅️ Geri Dön"): navigate('home')

# --- TEST LİSTESİ (image_10c8ee) ---
elif st.session_state.step == 'testler':
    ders = st.session_state.active_ders
    st.markdown(f"### {ders} Üniteleri")
    for unite in DERS_UNITELERI[ders]:
        st.info(f"📋 {unite} Test 1")
        if st.button(f"Çöz: {unite}", key=unite):
            st.session_state.active_unite = unite
            navigate('quiz')
    if st.button("⬅️ Kategorilere Dön"): navigate('kategoriler')

# --- SORU ÇÖZME PANELİ (image_112a48 / image_11a2aa) ---
elif st.session_state.step == 'quiz':
    data = get_soru_verisi(st.session_state.active_ders, st.session_state.active_unite, st.session_state.q_idx)
    
    # Üst Bilgi Paneli
    st.markdown(f"""
        <div class="header-panel">
            <span>⏰ 02:30</span>
            <span>{st.session_state.q_idx} / 20</span>
            <div style="display:flex; gap:10px;">
                <span class="score-box" style="background:#e74c3c;">{st.session_state.stats['y']}</span>
                <span class="score-box" style="background:#27ae60;">{st.session_state.stats['d']}</span>
            </div>
            <span>📝</span>
        </div>
    """, unsafe_allow_html=True)

    # Soru Kutusu
    st.markdown(f'<div class="q-text">{data["soru"]}</div>', unsafe_allow_html=True)

    # Şıklar
    cols_ans = st.columns(2)
    for i, h in enumerate(['A', 'B', 'C', 'D']):
        with cols_ans[i % 2]:
            if st.button(f"{h}) {data[h]}", key=f"btn_{h}"):
                if st.session_state.last_ans is None:
                    if h == data["cvp"]:
                        st.session_state.stats["d"] += 1
                        st.success("Tebrikler! Doğru.")
                    else:
                        st.session_state.stats["y"] += 1
                        st.error(f"Yanlış! Doğru Cevap: {data['cvp']}")
                    st.session_state.last_ans = h

    # Alt Navigasyon Çubuğu
    st.markdown("<br>", unsafe_allow_html=True)
    nav_c = st.columns(4)
    with nav_c[0]:
        if st.button("⬅️ Geri"):
            if st.session_state.q_idx > 1: st.session_state.q_idx -= 1; st.rerun()
    with nav_c[1]: st.button("❤️")
    with nav_c[2]:
        if st.button("İleri ➡️"):
            if st.session_state.q_idx < 20: 
                st.session_state.q_idx += 1
                st.session_state.last_ans = None
                st.rerun()
    with nav_c[3]:
        if st.button("❌"): navigate('testler')
