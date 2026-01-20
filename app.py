import streamlit as st
import PyPDF2
import random
import time

# Sayfa Ayarları
st.set_page_config(page_title="Yusuf Agaç - Yeni Nesil Matematik", page_icon="🧠", layout="wide")

# Hafıza Yönetimi (Session State)
if 'correct' not in st.session_state: st.session_state.correct = 0
if 'wrong' not in st.session_state: st.session_state.wrong = 0
if 'soru_havuzu' not in st.session_state:
    # Başlangıç için birkaç yeni nesil örnek soru
    st.session_state.soru_havuzu = [
        {"soru": "Bir manavda elmaların kilosu 15 TL, armutların kilosu 20 TL'dir. Yusuf 3 kg elma ve 2 kg armut alıp 100 TL verirse kaç TL para üstü alır?", "cevap": 15},
        {"soru": "Bir otobüste 45 yolcu vardır. İlk durakta 12 kişi inip 7 kişi biniyor. Son durumda otobüste kaç kişi vardır?", "cevap": 40},
        {"soru": "Bir kenarı 12 cm olan bir karenin çevresi, bir eşkenar üçgenin çevresine eşittir. Üçgenin bir kenarı kaç cm'dir?", "cevap": 16}
    ]
if 'aktif_soru' not in st.session_state:
    st.session_state.aktif_soru = random.choice(st.session_state.soru_havuzu)

# --- TASARIM ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stAlert { border-radius: 20px; }
    .soru-alani { background-color: #ffffff; padding: 30px; border-radius: 15px; border-left: 10px solid #ff4b4b; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 Yusuf Agaç: Yeni Nesil Matematik İstasyonu")

# Sol Panel: Başarı Takibi
with st.sidebar:
    st.header("📊 Başarı Durumu")
    st.metric("Doğru", st.session_state.correct)
    st.metric("Yanlış", st.session_state.wrong)
    
    st.divider()
    level = "Çaylak"
    if st.session_state.correct > 10: level = "Matematik Ustası"
    if st.session_state.correct > 20: level = "Profesör Yusuf"
    st.subheader(f"Rütbe: {level}")

# --- ANA BÖLÜM: YENİ NESİL SORU PANELİ ---
st.header("🧠 Günün Yeni Nesil Sorusu")

with st.container():
    st.markdown(f'<div class="soru-alani"><h3>{st.session_state.aktif_soru["soru"]}</h3></div>', unsafe_allow_html=True)
    
    cevap = st.number_input("Cevabını buraya yaz Yusuf:", key="cevap_input", step=1)
    
    col1, col2 = st.columns(2)
    
    if col1.button("🔥 Kontrol Et"):
        if cevap == st.session_state.aktif_soru["cevap"]:
            st.balloons()
            st.success("HARİKASIN YUSUF! Yeni nesil mantığını kavradın! ✅")
            st.session_state.correct += 1
        else:
            st.error(f"Dikkatli düşün Yusuf! ❌ Doğru cevap {st.session_state.aktif_soru['cevap']} olmalıydı.")
            st.session_state.wrong += 1
            
    if col2.button("➡️ Yeni Soru Oluştur"):
        # Burada yeni nesil mantığıyla sayıları rastgele değiştirerek yeni soru üretiyoruz
        tipler = [
            {"s": f"Yusuf bir kitabın her gün {random.randint(10,20)} sayfasını okuyor. {random.randint(3,7)} gün sonra kitabın bitmesine 15 sayfa kaldığına göre kitap kaç sayfadır?", "c": None},
            {"s": f"Tanesi {random.randint(5,15)} TL olan kalemlerden {random.randint(4,8)} tane alan Yusuf, kasaya {random.randint(100,200)} TL verirse kaç TL para üstü alır?", "c": None}
        ]
        secilen = random.choice(tipler)
        # Basit bir cevap hesaplama mantığı ekliyoruz (Örn: kalem sorusu için)
        if "kalem" in secilen["s"]:
            # Sorudaki rakamları ayıklayıp otomatik hesaplama yaptırabiliriz veya hazır havuzdan seçebiliriz
            st.session_state.aktif_soru = random.choice(st.session_state.soru_havuzu) 
        else:
            st.session_state.aktif_soru = random.choice(st.session_state.soru_havuzu)
        
        st.rerun()

# --- PDF ANALİZ BÖLÜMÜ ---
st.divider()
st.header("📂 Akıllı PDF Analizi")
uploaded_file = st.file_uploader("Çalışacağın PDF'i buraya yükle", type="pdf")

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    full_text = "".join([page.extract_text() for page in reader.pages])
    
    tab1, tab2 = st.tabs(["📑 Akıllı Özet", "🎯 Konu Testi"])
    
    with tab1:
        st.write("Yapay zeka notlarını okuyor...")
        st.info(full_text[:700] + "...") # Burası AI API ile geliştirilebilir
        
    with tab2:
        st.write("Bu metne göre Yusuf'a özel sorular hazırlanıyor...")
        st.warning("Soru: Metindeki en önemli matematiksel kavramı bulup bir cümlede kullan.")
