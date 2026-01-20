import streamlit as st
import random
import math

# Sayfa Yapılandırması
st.set_page_config(page_title="Yusuf Agaç - Görsel Asistan", page_icon="🎨", layout="wide")

# --- SİSTEM HAFIZASI ---
if 'cozulen_sorular' not in st.session_state: st.session_state.cozulen_sorular = []
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'aktif_soru_obj' not in st.session_state: st.session_state.aktif_soru_obj = None

# --- GÖRSEL ÇÖZÜM ÜRETİCİ (SVG) ---
def cozum_gorseli_ureti(tip, veri):
    if tip == "Saat":
        return f"""
        <svg width="150" height="150" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" stroke="black" stroke-width="2" fill="white" />
            <line x1="50" y1="50" x2="50" y2="15" stroke="black" stroke-width="3" /> <line x1="50" y1="50" x2="80" y2="50" stroke="red" stroke-width="3" /> <path d="M 50 40 A 10 10 0 0 1 60 50" fill="none" stroke="orange" stroke-width="2" />
        </svg>"""
    elif tip == "DogruAci":
        return f"""
        <svg width="200" height="100" viewBox="0 0 200 100">
            <line x1="10" y1="80" x2="190" y2="80" stroke="black" stroke-width="3" />
            <line x1="100" y1="80" x2="40" y2="20" stroke="red" stroke-width="2" stroke-dasharray="4" />
            <line x1="100" y1="80" x2="160" y2="20" stroke="red" stroke-width="2" stroke-dasharray="4" />
            <text x="80" y="95" font-size="10">180° / 3 = 60°</text>
        </svg>"""
    return ""

# --- YENİ NESİL SORU BANKASI ---
soru_bankasi = [
    {
        "id": 1, "tip": "Açı", "derece": 45,
        "soru": "Dik açının (90°) tam yarısı olan bir açı çizmek istiyoruz. Bu açı kaç derecedir?",
        "siklar": ["30", "45", "60", "90"], "cevap": "45",
        "analiz": "Bak Yusuf; 90'ı tam ortadan böldüğümüzde iki tane 45 elde ederiz.",
        "gorsel_tip": "AciBolme"
    },
    {
        "id": 2, "tip": "Saat",
        "soru": "Saat tam 15:00'i gösterdiğinde akrep ile yelkovan arasındaki açı nedir?",
        "siklar": ["Dar", "Dik", "Geniş", "Doğru"], "cevap": "Dik",
        "analiz": "Saat 3'te yelkovan tam tepede (12), akrep ise tam yandadır (3). Bu bir L şekli yani dik açıdır.",
        "gorsel_tip": "Saat"
    },
    {
        "id": 3, "tip": "DoğruAci",
        "soru": "Bir doğru açı (180°) 3 eş parçaya bölünürse her bir parçanın derecesi kaç olur?",
        "siklar": ["45", "60", "90", "120"], "cevap": "60",
        "analiz": "180 derecelik bir pastayı 3 kişiye eşit paylaştırırsan herkese 60 derece düşer.",
        "gorsel_tip": "DogruAci"
    }
]

def yeni_soru_sec():
    kalanlar = [s for s in soru_bankasi if s['id'] not in st.session_state.cozulen_sorular]
    st.session_state.aktif_soru_obj = random.choice(kalanlar) if kalanlar else "BITTI"

# --- ARAYÜZ ---
st.title("👨‍🏫 Yusuf Agaç: Görsel Asistanlı Test")

if st.session_state.aktif_soru_obj is None: yeni_soru_sec()

if st.session_state.aktif_soru_obj == "BITTI":
    st.balloons()
    st.success("Tüm sorular bitti! Yusuf sen bir harikasın! 🏆")
    if st.button("Tekrar Başla"):
        st.session_state.cozulen_sorular = []; st.session_state.puan = 0; yeni_soru_sec(); st.rerun()
else:
    s = st.session_state.aktif_soru_obj
    st.sidebar.metric("Puan", st.session_state.puan)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Soru")
        st.write(s['soru'])
        secim = st.radio("Cevabın:", s['siklar'], key=f"r_{s['id']}")
        
    if st.button("Cevabı Gönder"):
        if secim == s['cevap']:
            st.success("DOĞRU! 🌟")
            st.session_state.puan += 10
            st.session_state.cozulen_sorular.append(s['id'])
            st.button("Sıradaki Soru ➡️", on_click=yeni_soru_sec)
        else:
            st.error("Hatalı oldu, ama üzülme! İşte asistanın görsel çözümü:")
            st.markdown(f"""
            <div style="background:#e3f2fd; padding:20px; border-radius:15px;">
                <h4>🤖 Çözüm Şeması</h4>
                <p>{s['analiz']}</p>
                {cozum_gorseli_ureti(s['gorsel_tip'], None)}
            </div>
            """, unsafe_allow_html=True)
