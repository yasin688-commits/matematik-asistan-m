import streamlit as st
import random
import math

# Sayfa Yapılandırması
st.set_page_config(page_title="Yusuf Agaç - Başarı Analizi", page_icon="📈", layout="wide")

# --- SİSTEM HAFIZASI ---
if 'test_sorulari' not in st.session_state: st.session_state.test_sorulari = []
if 'mevcut_soru_index' not in st.session_state: st.session_state.mevcut_soru_index = 0
if 'yanlislar' not in st.session_state: st.session_state.yanlislar = [] # Yanlış yapılanları saklar
if 'dogru_sayisi' not in st.session_state: st.session_state.dogru_sayisi = 0

# --- GÖRSEL ÇÖZÜM ŞEMALARI ---
def cizim_asistani(tip, veri=None):
    if tip == "Açı":
        return """<svg width="100" height="60"><line x1="10" y1="50" x2="90" y2="50" stroke="black" stroke-width="3"/><line x1="10" y1="50" x2="50" y2="10" stroke="red" stroke-width="3"/><text x="10" y="45" font-size="10" fill="red">Açı</text></svg>"""
    elif tip == "Problem":
        return """<svg width="100" height="60"><rect x="10" y="10" width="30" height="40" fill="#add8e6" stroke="blue"/><rect x="50" y="10" width="30" height="40" fill="#add8e6" stroke="blue"/><text x="15" y="40" font-size="20">?</text></svg>"""
    return ""

# --- SORU MOTORU ---
def soru_uret():
    konular = [("Açılar", "Açı"), ("Paralarımız", "Problem"), ("Zaman", "Zaman")]
    yeni_test = []
    for i in range(1, 11):
        konu_adi, tip = random.choice(konular)
        a, b = random.randint(10, 50), random.randint(2, 9)
        
        if konu_adi == "Açılar":
            d = random.choice([30, 45, 60, 120])
            s = {"id": i, "soru": f"Ölçüsü {d} derece olan bir açıyı, 180 derecelik doğru açıya tamamlamak için kaç derece eklenmelidir?", 
                 "siklar": [str(180-d), str(90-d if 90>d else 20), "100", "80"], "cevap": str(180-d), "tip": "Açı",
                 "analiz": f"Doğru açı 180 derecedir. 180'den {d} çıkartırsak sonucu buluruz."}
        else:
            s = {"id": i, "soru": f"Tanesi {b} TL olan kalemlerden {a} tane alan Yusuf, toplam kaç TL ödeme yapar?", 
                 "siklar": [str(a*b), str(a+b), str(a*b+10), str(a*b-5)], "cevap": str(a*b), "tip": "Problem",
                 "analiz": f"Tane fiyatı ile adet sayısını çarpmalıyız: {a} x {b} = {a*b}"}
        
        random.shuffle(s["siklar"])
        yeni_test.append(s)
    return yeni_test

# --- ARAYÜZ ---
st.title("🚀 Yusuf Agaç: Akıllı Öğrenme Paneli")

# Yeni Test Butonu
if st.sidebar.button("♻️ Yeni 10 Soruluk Test Başlat"):
    st.session_state.test_sorulari = soru_uret()
    st.session_state.mevcut_soru_index = 0
    st.session_state.yanlislar = []
    st.session_state.dogru_sayisi = 0
    st.rerun()

if not st.session_state.test_sorulari:
    st.info("Yusuf, başlamak için sol taraftaki butona bas!")
elif st.session_state.mevcut_soru_index < 10:
    # --- TEST DEVAM EDİYOR ---
    soru = st.session_state.test_sorulari[st.session_state.mevcut_soru_index]
    st.subheader(f"Soru {st.session_state.mevcut_soru_index + 1}: {soru['tip']}")
    st.write(soru['soru'])
    
    secim = st.radio("Cevabını seç:", soru['siklar'], key=f"q_{st.session_state.mevcut_soru_index}")
    
    if st.button("Sonraki Soru ➡️"):
        if secim == soru['cevap']:
            st.session_state.dogru_sayisi += 1
        else:
            # Yanlış veriyi kaydet
            st.session_state.yanlislar.append({
                "soru": soru['soru'],
                "yusufun_cevabi": secim,
                "dogru_cevap": soru['cevap'],
                "analiz": soru['analiz'],
                "tip": soru['tip']
            })
        st.session_state.mevcut_soru_index += 1
        st.rerun()
else:
    # --- TEST BİTTİ: HATA ANALİZ MERKEZİ ---
    st.balloons()
    st.header("🏁 Test Sonucu ve Hata Analizi")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Doğru", st.session_state.dogru_sayisi)
    col2.metric("Yanlış", 10 - st.session_state.dogru_sayisi)
    col3.metric("Başarı", f"%{st.session_state.dogru_sayisi * 10}")

    if len(st.session_state.yanlislar) > 0:
        st.divider()
        st.subheader("🤖 Asistan Çözüm Merkezi (Hatalarını Öğren)")
        
        for i, hata in enumerate(st.session_state.yanlislar):
            with st.expander(f"❌ Soru {i+1} Analizini Gör"):
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.markdown(cizim_asistani(hata['tip']), unsafe_allow_html=True)
                with c2:
                    st.write(f"**Soru:** {hata['soru']}")
                    st.write(f"🔴 Senin Cevabın: {hata['yusufun_cevabi']}")
                    st.write(f"🟢 Doğru Cevap: {hata['dogru_cevap']}")
                    st.info(f"💡 **Asistan Diyor ki:** {hata['analiz']}")
    else:
        st.success("HİÇ YANLIŞIN YOK! Yusuf, sen bir matematik dâhisisin! 🏆")

    if st.button("Tekrar Test Çöz"):
        st.session_state.test_sorulari = []
        st.rerun()
