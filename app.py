import streamlit as st
import random
import time
import pandas as pd

# Plotly kontrolü (Hata almamak için güvenli import)
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# --- GLOBAL AYARLAR VE TASARIM ---
st.set_page_config(page_title="Yusuf AI: Ultra Learning", page_icon="💡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp { background: #F8FAFC; }
    
    .solution-card { background: #FFFFFF; border-radius: 20px; border-left: 8px solid #FF5A5F; padding: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin: 15px 0; }
    .stat-bubble { background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); color: white; padding: 20px; border-radius: 20px; text-align: center; }
    .question-box { background: #FFFFFF; border-radius: 25px; padding: 35px; text-align: center; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM HAFIZASI ---
if 'hafiza' not in st.session_state: st.session_state.hafiza = []
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'test_aktif' not in st.session_state: st.session_state.test_aktif = False

# --- YENİ NESİL SORU MOTORU ---
def soru_olustur(sinif, odak_konu=None):
    konular = ["Basamak Değeri", "Yol Problemleri", "Kesirler", "Örüntüler"]
    konu = odak_konu if odak_konu else random.choice(konular)
    s_id = random.randint(1000, 9999)
    
    if konu == "Yol Problemleri":
        yol = random.choice([60, 80, 100, 120])
        s = f"Yusuf bisikletiyle gideceği yolun önce yarısını, sonra kalan yolun yarısını gidiyor. Geriye 15 km yolu kaldığına göre yolun tamamı kaç km'dir?"
        c = "60"
        adimlar = ["1. Adım: Kalan yolun yarısı 15 ise, mola öncesi kalan yol 15x2=30 km'dir.", 
                   "2. Adım: Bu 30 km yolun yarısı olduğuna göre tamamı 30x2=60 km'dir."]
    elif konu == "Basamak Değeri":
        s = "4 basamaklı, rakamları farklı en büyük tek sayının binler basamağı ile birler basamağındaki rakamların basamak değerleri farkı kaçtır?"
        c = "8992" # 9875 -> 9000 - 5 = 8995 (Örnek mantık)
        adimlar = ["1. Adım: Rakamları farklı en büyük tek sayıyı bul: 9875", "2. Adım: 9000 (Binler) ve 5 (Birler) değerlerini belirle.", "3. Adım: Farkı hesapla: 9000 - 5 = 8995"]
    else:
        s = "Yusuf bir pastanın 1/4'ünü yedi. Kalan pastanın yarısını arkadaşına verdi. Geriye pastanın kaçta kaçı kaldı?"
        c = "3/8"
        adimlar = ["1. Adım: Kalan pastayı bul: 1 - 1/4 = 3/4", "2. Adım: Yarısını bulmak için 2'ye böl: 3/4 ÷ 2 = 3/8"]

    return {"id": s_id, "soru": s, "cevap": c, "konu": konu, "adimlar": adimlar, 
            "siklar": [c, "1/2", "15", "9000"]}

# --- ARAYÜZ ---
with st.sidebar:
    st.markdown(f"<div class='stat-bubble'>🏆 Başarı Puanı<br><h1>{st.session_state.puan}</h1></div>", unsafe_allow_html=True)
    st.divider()
    if PLOTLY_AVAILABLE and st.session_state.hafiza:
        df = pd.DataFrame(st.session_state.hafiza)
        fig = px.pie(df, names='durum', hole=0.4, color_discrete_sequence=['#10B981', '#EF4444'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("İstatistikler için daha fazla soru çözmelisin!")

if not st.session_state.test_aktif:
    st.title("🛡️ Yusuf AI: Ultra Learning")
    if st.button("Günlük Göreve Başla 🚀"):
        st.session_state.sorular = [soru_olustur("5") for _ in range(5)]
        st.session_state.test_aktif = True
        st.session_state.soru_no = 0
        st.session_state.yanlislar = []
        st.rerun()

elif st.session_state.soru_no < len(st.session_state.sorular):
    soru = st.session_state.sorular[st.session_state.soru_no]
    st.markdown(f"<div class='question-box'><h5>{soru['konu']}</h5><h3>{soru['soru']}</h3></div>", unsafe_allow_html=True)
    
    # WordBit tarzı hızlı seçim
    for sik in soru['siklar']:
        if st.button(f"🔹 {sik}", key=f"btn_{sik}_{soru['id']}", use_container_width=True):
            durum = "Doğru" if sik == soru['cevap'] else "Yanlış"
            if durum == "Doğru": st.session_state.puan += 20
            else: st.session_state.yanlislar.append(soru)
            st.session_state.hafiza.append({"konu": soru['konu'], "durum": durum})
            st.session_state.soru_no += 1
            st.rerun()

else:
    st.header("🏁 Gelişim Raporu")
    if st.session_state.yanlislar:
        for y in st.session_state.yanlislar:
            with st.expander(f"❌ {y['soru'][:40]}..."):
                st.markdown("<div class='solution-card'><h4>Photomath Çözüm Adımları</h4>", unsafe_allow_html=True)
                for adim in y['adimlar']:
                    st.write(f"👉 {adim}")
                st.markdown(f"<b>Doğru Cevap: {y['cevap']}</b></div>", unsafe_allow_html=True)
                
    if st.button("Tekrar Dene 🔄"):
        st.session_state.test_aktif = False
        st.rerun()
