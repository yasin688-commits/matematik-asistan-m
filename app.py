import streamlit as st
import random
import math

# Sayfa Yapılandırması
st.set_page_config(page_title="Yusuf Agaç - Yapay Zeka Testi", page_icon="🤖", layout="wide")

# --- SİSTEM HAFIZASI ---
if 'test_sorulari' not in st.session_state:
    st.session_state.test_sorulari = []
if 'mevcut_soru_index' not in st.session_state:
    st.session_state.mevcut_soru_index = 0
if 'dogru_sayisi' not in st.session_state:
    st.session_state.dogru_sayisi = 0

# --- YAPAY ZEKA SORU ÜRETİCİ (Dinamik Motor) ---
def soru_uret():
    konular = ["Açılar", "Kesirler", "Alan Ölçme", "Doğal Sayılar", "Zaman Ölçme"]
    yeni_test = []
    
    for i in range(1, 11):
        konu = random.choice(konular)
        # Yapay zeka mantığıyla sayıları ve senaryoları her seferinde farklı oluşturuyoruz
        a = random.randint(5, 50)
        b = random.randint(2, 10)
        
        if konu == "Açılar":
            derece = random.choice([30, 45, 60, 90, 120, 150])
            s = {
                "id": i,
                "soru": f"Yusuf bir kağıda {derece} derecelik bir açı çiziyor. Bu açıyı 180 derecelik bir doğru açıya tamamlamak için kaç derece daha eklemelidir?",
                "siklar": [str(180-derece), str(90-derece if 90>derece else 10), "45", "100"],
                "cevap": str(180-derece),
                "tip": "Açı",
                "analiz": f"Doğru açı 180 derecedir. 180 - {derece} = {180-derece} eder."
            }
        elif konu == "Doğal Sayılar":
            s = {
                "id": i,
                "soru": f"Yusuf'un biriktirdiği {a*b} TL parası var. Tanesi {a} TL olan kitaplardan kaç tane alabilir?",
                "siklar": [str(b), str(b+2), str(b-1), "5"],
                "cevap": str(b),
                "tip": "Problem",
                "analiz": f"{a*b} / {a} = {b} tane alabilir."
            }
        else: # Genel Mantık
            s = {
                "id": i,
                "soru": f"Yusuf her gün {a} sayfa kitap okuyor. 10. günün sonunda toplam kaç sayfa okumuş olur?",
                "siklar": [str(a*10), str(a*10-5), str(a*5), str(a*20)],
                "cevap": str(a*10),
                "tip": "Zaman/Hız",
                "analiz": f"Her gün {a} ise, 10 günde {a} x 10 = {a*10} olur."
            }
        
        random.shuffle(s["siklar"]) # Şıkları karıştır
        yeni_test.append(s)
    
    return yeni_test

# --- ANA EKRAN ---
st.title("🤖 Yusuf Agaç: 10 Soruluk Akıllı Test")

# Testi Başlat/Yenile
if not st.session_state.test_sorulari or st.sidebar.button("♻️ Yeni 10 Soruluk Test Üret"):
    st.session_state.test_sorulari = soru_uret()
    st.session_state.mevcut_soru_index = 0
    st.session_state.dogru_sayisi = 0
    st.rerun()

# --- TEST EKRANI ---
if st.session_state.mevcut_soru_index < 10:
    soru = st.session_state.test_sorulari[st.session_state.mevcut_soru_index]
    
    st.sidebar.subheader(f"Soru: {st.session_state.mevcut_soru_index + 1} / 10")
    st.sidebar.progress((st.session_state.mevcut_soru_index + 1) * 10)
    
    with st.container():
        st.markdown(f"### 📍 {soru['tip']}")
        st.info(soru['soru'])
        
        secim = st.radio("Yusuf, cevabını seç:", soru['siklar'], key=f"q_{soru['id']}_{st.session_state.mevcut_soru_index}")
        
        if st.button("Onayla ve Sonraki Soru ➡️"):
            if secim == soru['cevap']:
                st.toast("Harikasın Yusuf! +1 Puan", icon="✅")
                st.session_state.dogru_sayisi += 1
            else:
                st.toast("Dikkatli ol Yusuf!", icon="❌")
                st.error(f"Doğru Cevap: {soru['cevap']}\n\nÇözüm: {soru['analiz']}")
                time_sleep = 2 # Yusuf'un çözümü okuması için süre
            
            st.session_state.mevcut_soru_index += 1
            st.rerun()

else:
    # --- TEST SONUCU ---
    st.balloons()
    st.header("🏁 Test Bitti!")
    st.success(f"Tebrikler Yusuf! 10 soruda {st.session_state.dogru_sayisi} doğru yaptın.")
    
    basari = (st.session_state.dogru_sayisi / 10) * 100
    st.write(f"Başarı Oranın: %{basari}")
    
    if st.button("🎉 Yeni Bir Teste Başla"):
        st.session_state.test_sorulari = []
        st.rerun()

# --- ASİSTAN GÖRSELLERİ (Hata Korumalı) ---
if st.session_state.mevcut_soru_index < 10:
    with st.expander("🤖 Asistan Çizimi"):
        st.write("Soruya göre görsel şema hazırlanıyor...")
        # Açı görseli ekleme (Eğer soru açıysa)
        if st.session_state.test_sorulari[st.session_state.mevcut_soru_index]['tip'] == "Açı":
            st.markdown('<svg width="100" height="100"><line x1="10" y1="90" x2="90" y2="90" stroke="black" stroke-width="3"/><line x1="10" y1="90" x2="10" y2="10" stroke="black" stroke-width="3"/></svg>', unsafe_allow_html=True)
