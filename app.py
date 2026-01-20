import streamlit as st
import random
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Yusuf Agaç Eğitim Akademisi", page_icon="🎓", layout="wide")

# --- SİSTEM HAFIZASI ---
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'test_aktif' not in st.session_state: st.session_state.test_aktif = False
if 'soru_no' not in st.session_state: st.session_state.soru_no = 0
if 'yanlislar' not in st.session_state: st.session_state.yanlislar = []

# --- DİNAMİK SORU MOTORU ---
def ai_soru_uret(sinif, ders, zorluk):
    # Zorluk katsayısı
    n1, n2 = (1, 10) if zorluk == "Kolay" else (10, 50) if zorluk == "Orta" else (50, 200)
    
    # Sınıf seviyesine göre senaryo ve konu ayarlama
    if ders == "Matematik":
        if sinif <= 4: # İlkokul
            a, b = random.randint(n1, n2), random.randint(n1, n2)
            soru = f"{a} + {b} işleminin sonucu kaçtır?"
            cevap = str(a + b)
            analiz = f"İlkokul seviyesi toplama: {a} ile {b} toplandığında {cevap} eder."
        elif sinif <= 8: # Ortaokul
            a = random.randint(n1, n2)
            soru = f"Bir açının ölçüsü {a} derecedir. Bu açının tümler açısı (toplamı 90 olan) kaç derecedir?"
            cevap = str(90 - a if 90 > a else a + 10)
            analiz = f"Tümler açılar birbirini 90 dereceye tamamlar. 90 - {a} = {cevap}."
        else: # Lise
            a = random.randint(2, 5)
            soru = f"f(x) = {a}x + 10 fonksiyonunda f(2) değeri kaçtır?"
            cevap = str(a * 2 + 10)
            analiz = f"x yerine 2 koyduğumuzda: {a} * 2 + 10 = {cevap} olur."
    
    elif ders == "Fen Bilimleri":
        soru_havuzu = [
            {"s": "Güneş sistemindeki en büyük gezegen hangisidir?", "c": "Jüpiter", "a": "Jüpiter dev bir gaz gezegenidir."},
            {"s": "Suyun kimyasal formülü nedir?", "c": "H2O", "a": "2 Hidrojen ve 1 Oksijen atomundan oluşur."},
            {"s": "Hücrenin enerji santrali hangisidir?", "c": "Mitokondri", "a": "Hücre solunumu burada gerçekleşir."}
        ]
        secilen = random.choice(soru_havuzu)
        return {"s": secilen["s"], "c": secilen["c"], "siklar": [secilen["c"], "Mars", "Oksijen", "Çekirdek"], "tip": ders, "analiz": secilen["a"]}

    # Şık Karıştırma Mantığı
    yanlislar = [str(int(cevap)+random.randint(1,5)), str(int(cevap)-random.randint(1,5)), "0"] if cevap.isdigit() else ["Cevap B", "Cevap C", "Cevap D"]
    butun_siklar = [cevap] + yanlislar
    random.shuffle(butun_siklar)
    
    return {"s": soru, "c": cevap, "siklar": butun_siklar, "tip": ders, "analiz": analiz}

# --- ARAYÜZ ---
st.title("🚀 Yusuf Agaç: Kişiselleştirilmiş Eğitim Üssü")

# 1. ADIM: AYARLAR (Sınıf, Ders, Zorluk)
if not st.session_state.test_aktif:
    col_setup1, col_setup2, col_setup3 = st.columns(3)
    
    with col_setup1:
        sinif = st.selectbox("Sınıfını Seç:", [f"{i}. Sınıf" for i in range(1, 13)])
        sinif_int = int(sinif.split('.')[0])
        
    with col_setup2:
        ders = st.selectbox("Ders Seç:", ["Matematik", "Fen Bilimleri", "Türkçe"])
        
    with col_setup3:
        zorluk = st.select_slider("Zorluk Seviyesi:", options=["Kolay", "Orta", "Zor"])

    if st.button("🏁 Eğitimi Başlat"):
        st.session_state.test_sorulari = [ai_soru_uret(sinif_int, ders, zorluk) for _ in range(10)]
        st.session_state.test_aktif = True
        st.session_state.soru_no = 0
        st.session_state.yanlislar = []
        st.rerun()

# 2. ADIM: SORU EKRANI
elif st.session_state.soru_no < 10:
    soru = st.session_state.test_sorulari[st.session_state.soru_no]
    
    st.subheader(f"Soru {st.session_state.soru_no + 1} / 10")
    st.info(soru['s'])
    
    cevap = st.radio("Cevabını Seç:", soru['siklar'], index=None, key=f"q_{st.session_state.soru_no}")
    
    if st.button("Onayla ve İlerle"):
        if cevap is None:
            st.warning("Lütfen bir şık seç!")
        else:
            if cevap == soru['c']:
                st.session_state.puan += 10
                st.toast("Harikasın! +10 Puan", icon="✅")
            else:
                st.session_state.yanlislar.append(soru)
                st.toast("Öğrenmek için güzel bir fırsat!", icon="💡")
            
            st.session_state.soru_no += 1
            st.rerun()

# 3. ADIM: ANALİZ EKRANI
else:
    st.header("🏁 Görev Tamamlandı!")
    st.metric("Toplam Puan", st.session_state.puan)
    
    if st.session_state.yanlislar:
        st.subheader("🤖 Asistan Çözüm Analizi")
        for y in st.session_state.yanlislar:
            with st.expander(f"❌ {y['s'][:40]}..."):
                st.write(f"**Doğru Cevap:** {y['c']}")
                st.info(f"**Nasıl Çözülür?** {y['analiz']}")
                
    if st.button("🔄 Yeni Bir Seviye Seç"):
        st.session_state.test_aktif = False
        st.rerun()
