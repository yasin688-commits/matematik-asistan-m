import streamlit as st
import random
import math
import PyPDF2

# Sayfa Yapılandırması
st.set_page_config(page_title="Yusuf Agaç - Görsel Matematik", page_icon="🎓", layout="wide")

# --- SİSTEM HAFIZASI ---
if 'cozulen_sorular' not in st.session_state: st.session_state.cozulen_sorular = []
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'aktif_soru_obj' not in st.session_state: st.session_state.aktif_soru_obj = None

# --- GÖRSEL ÇÖZÜM ÜRETİCİ (Hata Vermeyen Yapı) ---
def cozum_gorseli_goster(gorsel_tip):
    if gorsel_tip == "Saat":
        st.markdown("""
        <svg width="150" height="150" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" stroke="black" stroke-width="2" fill="white" />
            <line x1="50" y1="50" x2="50" y2="15" stroke="black" stroke-width="3" /> <line x1="50" y1="50" x2="80" y2="50" stroke="red" stroke-width="3" /> <path d="M 50 40 A 10 10 0 0 1 60 50" fill="none" stroke="orange" stroke-width="2" />
        </svg>
        """, unsafe_allow_html=True)
    elif gorsel_tip == "DogruAci":
        st.markdown("""
        <svg width="200" height="100" viewBox="0 0 200 100">
            <line x1="10" y1="80" x2="190" y2="80" stroke="black" stroke-width="3" />
            <line x1="100" y1="80" x2="40" y2="20" stroke="red" stroke-width="2" stroke-dasharray="4" />
            <line x1="100" y1="80" x2="160" y2="20" stroke="red" stroke-width="2" stroke-dasharray="4" />
            <text x="60" y="95" font-size="12" fill="blue">180° / 3 Parça = 60°</text>
        </svg>
        """, unsafe_allow_html=True)
    elif gorsel_tip == "AciBolme":
        st.markdown("""
        <svg width="150" height="150" viewBox="0 0 100 100">
            <line x1="20" y1="80" x2="80" y2="80" stroke="black" stroke-width="3" />
            <line x1="20" y1="80" x2="20" y2="20" stroke="black" stroke-width="3" />
            <line x1="20" y1="80" x2="60" y2="40" stroke="red" stroke-width="3" />
            <text x="25" y="70" font-size="10" fill="red">45°</text>
        </svg>
        """, unsafe_allow_html=True)

# --- SORU BANKASI ---
soru_bankasi = [
    {
        "id": 1, "tip": "Açı", "soru": "Bir dik açıyı (90°) tam ortasından ikiye bölersek, oluşan her bir açının ölçüsü kaç derece olur?",
        "siklar": ["30", "45", "60", "90"], "cevap": "45",
        "analiz": "Yusuf, dik açı bir L harfidir. Onu tam ortadan böldüğümüzde 90'ın yarısı olan 45 dereceyi buluruz.",
        "gorsel_tip": "AciBolme"
    },
    {
        "id": 2, "tip": "Saat", "soru": "Saat tam 15:00'i gösterirken akrep ve yelkovan arasında oluşan açı hangisidir?",
        "siklar": ["Dar", "Dik", "Geniş", "Doğru"], "cevap": "Dik",
        "analiz": "Saat 3'te akrep 3'ü, yelkovan 12'yi gösterir. Aralarında tam bir köşe (90°) oluşur.",
        "gorsel_tip": "Saat"
    },
    {
        "id": 3, "tip": "Mantık", "soru": "Bir doğru açı (180°) üzerinde 3 tane eşit büyüklükte açı oluşturulursa, bir tanesi kaç derece olur?",
        "siklar": ["45", "60", "90", "180"], "cevap": "60",
        "analiz": "Düz bir çizgiyi (180°) 3 eşit parçaya ayırmak için 180'i 3'e böleriz: 180 / 3 = 60.",
        "gorsel_tip": "DogruAci"
    }
]

def yeni_soru_sec():
    kalanlar = [s for s in soru_bankasi if s['id'] not in st.session_state.cozulen_sorular]
    if kalanlar: st.session_state.aktif_soru_obj = random.choice(kalanlar)
    else: st.session_state.aktif_soru_obj = "BITTI"

# --- ANA PROGRAM ---
st.title("👨‍🏫 Yusuf Agaç: Görsel Matematik Dünyası")

# PDF Yükleme Bölümü (En Üstte)
with st.expander("📚 Kitap/PDF Yükle ve Özetle"):
    uploaded_file = st.file_uploader("PDF dosyanı buraya bırak Yusuf", type="pdf")
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = "".join([page.extract_text() for page in pdf_reader.pages])
        st.success("PDF Başarıyla Okundu!")
        if st.button("Özet Çıkar ve Soru Sor"):
            st.info(f"📖 **Özet:** {text[:500]}...")
            st.warning("❓ **Soru:** Bu okuduğun metne göre en önemli kural nedir?")

st.divider()

if st.session_state.aktif_soru_obj is None: yeni_soru_sec()

if st.session_state.aktif_soru_obj == "BITTI":
    st.balloons()
    st.success("Tüm yeni nesil soruları başarıyla tamamladın Yusuf! 🏆")
    if st.button("Testi Tekrar Başlat"):
        st.session_state.cozulen_sorular = []; st.session_state.puan = 0; yeni_soru_sec(); st.rerun()
else:
    s = st.session_state.aktif_soru_obj
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader(f"📍 Soru Türü: {s['tip']}")
        st.markdown(f"**{s['soru']}**")
        secim = st.radio("Cevabını Seç:", s['siklar'], key=f"q_{s['id']}")
        
        if st.button("Cevabı Onayla"):
            if secim == s['cevap']:
                st.balloons()
                st.success("Harikasın Yusuf! Doğru cevap. 🎉")
                st.session_state.puan += 10
                st.session_state.cozulen_sorular.append(s['id'])
                st.button("Sıradaki Soruya Geç ➡️", on_click=yeni_soru_sec)
            else:
                st.error("Bu sefer olmadı ama asistanın görsel çözümü burada! 👇")
                st.info(s['analiz'])
                cozum_gorseli_goster(s['gorsel_tip'])

# Yan Panel Bilgileri
st.sidebar.header("🏆 Yusuf'un Karnesi")
st.sidebar.metric("Toplam Puan", st.session_state.puan)
st.sidebar.write(f"Kalan Soru: {len(soru_bankasi) - len(st.session_state.cozulen_sorular)}")
