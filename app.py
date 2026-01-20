import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px # İstatistikleri görselleştirmek için

# --- GLOBAL AYARLAR VE TASARIM (Photomath & WordBit Style) ---
st.set_page_config(page_title="Yusuf AI: Akıllı Akademi", page_icon="💡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp { background: #F7F9FC; }
    
    /* Photomath Style Kartlar */
    .solution-card { background: white; border-radius: 20px; border-left: 10px solid #FF5A5F; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin: 15px 0; }
    .stat-bubble { background: linear-gradient(135deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%); color: white; padding: 20px; border-radius: 25px; text-align: center; font-weight: bold; }
    
    /* WordBit Style Soru Kutusu */
    .question-box { background: #FFFFFF; border: 2px solid #E0E0E0; border-radius: 30px; padding: 40px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.02); }
    .option-btn { background: #FFFFFF; border: 2px solid #E0E0E0; border-radius: 15px; padding: 15px; width: 100%; transition: 0.3s; cursor: pointer; }
    .option-btn:hover { border-color: #4158D0; background: #F0F2FF; }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM HAFIZASI VE ANALİZ ---
if 'hafiza' not in st.session_state: st.session_state.hafiza = []
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'test_aktif' not in st.session_state: st.session_state.test_aktif = False
if 'analiz_modu' not in st.session_state: st.session_state.analiz_modu = False

# --- YENİ NESİL SORU BANKASI (Photomath Mantığı) ---
def soru_olustur(sinif, odak_konu=None):
    konular = ["Basamak Değeri", "Yol Problemleri", "Kesirler", "Örüntüler", "Mantık"]
    konu = odak_konu if odak_konu else random.choice(konular)
    s_id = random.randint(1000, 9999)
    
    if konu == "Yol Problemleri":
        hiz = random.randint(60, 90)
        sure = random.randint(2, 5)
        s = f"Bir araç saatte {hiz} km hızla {sure} saat gidiyor. Yolun yarısında mola verdiğine göre yolun tamamı kaç km'dir?"
        c = str(hiz * sure * 2)
        adimlar = [f"1. Adım: Gidilen yolu bul -> {hiz} x {sure} = {hiz*sure} km.", 
                   f"2. Adım: Bu yol yarısıysa, tamamı için 2 ile çarp -> {hiz*sure} x 2 = {c} km."]
    elif konu == "Basamak Değeri":
        n = random.randint(1000, 9999)
        s = f"{n} sayısının yüzler basamağındaki rakamın basamak değeri ile onlar basamağındaki rakamın sayı değerinin toplamı kaçtır?"
        yuzler = (n // 100) % 10
        onlar = (n // 10) % 10
        c = str((yuzler * 100) + onlar)
        adimlar = [f"1. Yüzler basamağı: {yuzler} (Değeri: {yuzler*100})", 
                   f"2. Onlar basamağı: {onlar} (Sayı değeri kendisidir)", f"3. Toplam: {yuzler*100} + {onlar} = {c}"]
    else:
        s = "3 - 7 - 11 - 15 - ? örüntüsünde soru işareti yerine ne gelmelidir?"
        c = "19"
        adimlar = ["1. Artış miktarını bul: 7 - 3 = 4", "2. Son sayıya artışı ekle: 15 + 4 = 19"]

    return {"id": s_id, "soru": s, "cevap": c, "konu": konu, "adimlar": adimlar, 
            "siklar": random.sample([c, str(int(c)+10), str(int(c)-5), str(int(c)*2)], 4)}

# --- ANA ARAYÜZ ---
with st.sidebar:
    st.markdown("<div class='stat-bubble'>🏆 Yusuf'un Başarı Puanı<br><h1>{}</h1></div>".format(st.session_state.puan), unsafe_allow_html=True)
    st.divider()
    if st.session_state.hafiza:
        df = pd.DataFrame(st.session_state.hafiza)
        fig = px.pie(df, names='durum', color='durum', color_discrete_map={'Doğru':'#00C897', 'Yanlış':'#FF5A5F'}, hole=0.5)
        st.plotly_chart(fig, use_container_width=True)

if not st.session_state.test_aktif:
    st.title("🛡️ Yusuf AI: Geleceğin Bilgini")
    st.info("WordBit Metodu: Her gün 5 soru çözerek zihnini zinde tut!")
    
    col1, col2 = st.columns(2)
    with col1:
        sinif = st.selectbox("Sınıf Seç", ["4. Sınıf", "5. Sınıf", "6. Sınıf"])
    with col2:
        # Yapay Zeka Analizi
        if st.session_state.hafiza:
            yanlislar = [h['konu'] for h in st.session_state.hafiza if h['durum'] == 'Yanlış']
            if yanlislar:
                odak = max(set(yanlislar), key=yanlislar.count)
                st.warning(f"🤖 AI Önerisi: **{odak}** konusunda zayıfsın. Buraya odaklanalım mı?")
                if st.button("AI Odaklı Testi Başlat"):
                    st.session_state.sorular = [soru_olustur(sinif, odak) for _ in range(5)]
                    st.session_state.test_aktif = True
                    st.session_state.soru_no = 0
                    st.session_state.yanlislar = []
                    st.rerun()

    if st.button("Normal Karışık Test Başlat 🚀"):
        st.session_state.sorular = [soru_olustur(sinif) for _ in range(5)]
        st.session_state.test_aktif = True
        st.session_state.soru_no = 0
        st.session_state.yanlislar = []
        st.rerun()

elif st.session_state.soru_no < len(st.session_state.sorular):
    # SORU EKRANI (WordBit Style)
    soru = st.session_state.sorular[st.session_state.soru_no]
    st.progress((st.session_state.soru_no + 1) * 20)
    
    st.markdown(f"<div class='question-box'><p style='color:#666;'>{soru['konu']}</p><h2>{soru['soru']}</h2></div>", unsafe_allow_html=True)
    
    # Şıklar
    cols = st.columns(2)
    for i, sik in enumerate(soru['siklar']):
        if cols[i % 2].button(sik, key=f"btn_{i}_{soru['id']}", use_container_width=True):
            durum = "Doğru" if sik == soru['cevap'] else "Yanlış"
            if durum == "Doğru": st.session_state.puan += 20
            else: st.session_state.yanlislar.append(soru)
            
            st.session_state.hafiza.append({"konu": soru['konu'], "durum": durum})
            st.session_state.soru_no += 1
            st.rerun()

    if st.button("🏳️ Testi Bitir"):
        st.session_state.soru_no = 100
        st.rerun()

else:
    # ANALİZ EKRANI (Photomath Style)
    st.balloons()
    st.header("🏁 Gelişim Raporun")
    
    if st.session_state.yanlislar:
        st.subheader("🤖 Photomath Stili Adım Adım Çözümler")
        for y in st.session_state.yanlislar:
            with st.expander(f"❌ {y['soru'][:50]}..."):
                st.markdown(f"<div class='solution-card'><h3>Çözüm Yolu</h3>", unsafe_allow_html=True)
                for adim in y['adimlar']:
                    st.write(adim)
                st.markdown(f"<b>Doğru Cevap: {y['cevap']}</b></div>", unsafe_allow_html=True)
                
                
                if st.button(f"'{y['konu']}' Konusundan 1 Soru Daha Çöz", key=f"extra_{y['id']}"):
                    # Anlık benzer soru üretimi
                    st.session_state.sorular.append(soru_olustur("5. Sınıf", y['konu']))
                    st.session_state.soru_no = len(st.session_state.sorular) - 1
                    st.rerun()

    if st.button("Ana Sayfaya Dön"):
        st.session_state.test_aktif = False
        st.rerun()
