import streamlit as st
import random
import math

# Sayfa Yapılandırması
st.set_page_config(page_title="Yusuf Agaç - Yeni Nesil Test", page_icon="📝", layout="wide")

# --- HAFIZA VE SİSTEM YÖNETİMİ ---
if 'cozulen_sorular' not in st.session_state:
    st.session_state.cozulen_sorular = []
if 'puan' not in st.session_state:
    st.session_state.puan = 0
if 'aktif_soru_obj' not in st.session_state:
    st.session_state.aktif_soru_obj = None

# --- YENİ NESİL SORU BANKASI (Yapay Zeka Mantığıyla Hazırlanmış) ---
# Buradaki her soru birer nesne gibi yapılandırılmıştır.
soru_bankasi = [
    {
        "id": 1,
        "tip": "Açı",
        "derece": 45,
        "soru": "Bir açının ölçüsü, dik açının tam yarısına eşittir. Bu açı kaç derecedir?",
        "siklar": ["30", "45", "60", "90"],
        "cevap": "45",
        "analiz": "Dik açı 90 derecedir. Yarısı 90 / 2 = 45 eder."
    },
    {
        "id": 2,
        "tip": "Mantık",
        "soru": "Yusuf, elindeki 180 derecelik doğru açıyı 3 eşit parçaya bölüyor. Her bir parçanın açı türü ne olur?",
        "siklar": ["Geniş Açı", "Dik Açı", "Dar Açı", "Doğru Açı"],
        "cevap": "Dar Açı",
        "analiz": "180 / 3 = 60 derecedir. 60 derece 90'dan küçük olduğu için Dar Açı'dır."
    },
    {
        "id": 3,
        "tip": "Açı",
        "derece": 120,
        "soru": "Görseldeki açıya kaç derece daha eklenirse bir 'Doğru Açı' (180°) elde edilir?",
        "siklar": ["40", "50", "60", "80"],
        "cevap": "60",
        "analiz": "Doğru açı 180 derecedir. 180 - 120 = 60 derece eklenmelidir."
    },
    {
        "id": 4,
        "tip": "Mantık",
        "soru": "Bir saatte akrep ile yelkovan tam saat 15:00'i gösterirken aralarındaki açı kaç derecedir?",
        "siklar": ["45", "90", "120", "180"],
        "cevap": "90",
        "analiz": "Saat 3'te akrep 3'ü, yelkovan 12'yi gösterir. Bu bir dik açıdır (90°)."
    }
]

# --- YARDIMCI FONKSİYONLAR ---
def aci_ciz_modern(derece):
    rad = math.radians(derece)
    x = 150 + 80 * math.cos(-rad)
    y = 150 + 80 * math.sin(-rad)
    return f"""
    <svg width="300" height="200" viewBox="0 0 300 200" style="background:#fff; border-radius:15px; border:1px solid #ddd;">
        <line x1="150" y1="150" x2="250" y2="150" style="stroke:#333; stroke-width:4" />
        <line x1="150" y1="150" x2="{x}" y2="{y}" style="stroke:red; stroke-width:5" />
        <path d="M 170 150 A 20 20 0 0 0 {150+20*math.cos(-rad)} {150+20*math.sin(-rad)}" fill="none" stroke="orange" stroke-width="2"/>
    </svg>"""

def yeni_soru_sec():
    kalanlar = [s for s in soru_bankasi if s['id'] not in st.session_state.cozulen_sorular]
    if kalanlar:
        st.session_state.aktif_soru_obj = random.choice(kalanlar)
    else:
        st.session_state.aktif_soru_obj = "BITTI"

# --- ARAYÜZ ---
st.title("🚀 Yusuf Agaç: Yeni Nesil Matematik Testi")

if st.session_state.aktif_soru_obj is None:
    yeni_soru_sec()

if st.session_state.aktif_soru_obj == "BITTI":
    st.balloons()
    st.success("Tebrikler Yusuf! Tüm soruları bitirdin. 🏆")
    if st.button("Testi Sıfırla"):
        st.session_state.cozulen_sorular = []
        yeni_soru_sec()
        st.rerun()
else:
    soru = st.session_state.aktif_soru_obj
    
    # Soru Alanı
    st.info(f"📍 Konu: {soru['tip']}")
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        if soru['tip'] == "Açı" and 'derece' in soru:
            st.markdown(aci_ciz_modern(soru['derece']), unsafe_allow_html=True)
            st.write(f"*(Görseldeki açı {soru['derece']} derecedir)*")
        else:
            st.image("https://img.icons8.com/clouds/200/brainstorming.png", width=150)

    with col2:
        st.subheader(soru['soru'])
        secim = st.radio("Cevabını Seç Yusuf:", soru['siklar'], key=f"radio_{soru['id']}")
        
        if st.button("Cevabı Onayla"):
            if secim == soru['cevap']:
                st.success("DOĞRU! Harikasın Yusuf. 🎉")
                st.session_state.puan += 10
            else:
                st.error(f"Yanlış Cevap! Doğru cevap: {soru['cevap']}")
                with st.expander("📚 Asistan Çözümü Gör"):
                    st.write(soru['analiz'])
            
            st.session_state.cozulen_sorular.append(soru['id'])
            time_wait = st.empty()
            st.button("Sonraki Soruya Geç ➡️", on_click=yeni_soru_sec)

# Sol Panel (Skor)
with st.sidebar:
    st.header("🏆 Yusuf'un Başarısı")
    st.write(f"Toplam Puan: **{st.session_state.puan}**")
    st.write(f"Çözülen Soru: **{len(st.session_state.cozulen_sorular)} / {len(soru_bankasi)}**")
    st.progress(len(st.session_state.cozulen_sorular) / len(soru_bankasi))
