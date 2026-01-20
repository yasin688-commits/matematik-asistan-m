import streamlit as st
import random
import time
import math

# --- SAYFA VE STİL AYARLARI ---
st.set_page_config(page_title="Yusuf'un Matematik Üssü", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .rutbe-karti { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; border-bottom: 5px solid #4CAF50; }
    .soru-box { background: white; padding: 25px; border-radius: 20px; border-left: 10px solid #2196F3; margin-bottom: 20px; }
    .stButton>button { border-radius: 50px; height: 3em; font-weight: bold; transition: all 0.3s; }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM HAFIZASI ---
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'test_aktif' not in st.session_state: st.session_state.test_aktif = False
if 'soru_no' not in st.session_state: st.session_state.soru_no = 0
if 'yanlislar' not in st.session_state: st.session_state.yanlislar = []
if 'zaman_baslangic' not in st.session_state: st.session_state.zaman_baslangic = 0

# --- RÜTBE HESAPLAMA ---
def rutbe_bul(puan):
    if puan < 50: return "Çaylak Matematikçi 🛡️", "#7f8c8d"
    if puan < 150: return "Sayı Savaşçısı ⚔️", "#27ae60"
    if puan < 300: return "Açı Ustası 📐", "#2980b9"
    if puan < 500: return "Problem Çözücü 🧠", "#8e44ad"
    return "Sayıların Efendisi 👑", "#f1c40f"

# --- SORU MOTORU (ŞIKLARI KARIŞTIRAN YAPI) ---
def yeni_nesil_soru_uret():
    konu = random.choice(["Açılar", "Market Problemi", "Zaman"])
    soru_verisi = {}
    
    if konu == "Açılar":
        d = random.choice([30, 45, 60, 90, 120])
        soru_verisi = {
            "s": f"Yusuf bir pergel ile {d} derecelik bir açı çiziyor. Öğretmeni bu açıyı 'Doğru Açıya' (180°) tamamlamasını istiyor. Yusuf kaç derece daha çizmelidir?",
            "c": str(180-d), 
            "yanlislar": [str(180-d-10), "90", "180"], 
            "tip": "Açı",
            "analiz": f"Doğru açı 180 derecedir. 180 - {d} = {180-d} sonucuna ulaşırız."
        }
    elif konu == "Market Problemi":
        f = random.randint(5, 15)
        m = random.randint(3, 7)
        toplam = f * m
        soru_verisi = {
            "s": f"Yusuf tanesi {f} TL olan kalemlerden {m} tane alıyor. Kasaya 100 TL verirse ne kadar para üstü alır?",
            "c": str(100-toplam), 
            "yanlislar": [str(toplam), str(100-toplam+10), "50"], 
            "tip": "Problem",
            "analiz": f"Önce harcanan para: {f}x{m}={toplam} TL. Para üstü: 100-{toplam}={100-toplam} TL."
        }
    else:
        soru_verisi = {
            "s": "Bir günün 1/4'ünü uyuyarak geçiren Yusuf, kaç saat uyumuştur?",
            "c": "6", 
            "yanlislar": ["8", "4", "12"], 
            "tip": "Zaman",
            "analiz": "Bir gün 24 saattir. 24'ün 1/4'ü 24/4 = 6 saattir."
        }
    
    # Şıkları birleştir ve KARIŞTIR
    butun_siklar = [soru_verisi["c"]] + soru_verisi["yanlislar"]
    random.shuffle(butun_siklar)
    soru_verisi["siklar"] = butun_siklar
    return soru_verisi

# --- ANA EKRAN ---
st.title("🛡️ Yusuf'un Matematik Macera Üssü")

with st.sidebar:
    rutbe, renk = rutbe_bul(st.session_state.puan)
    st.markdown(f"<div class='rutbe-karti'><h3>{rutbe}</h3><h1 style='color:{renk};'>{st.session_state.puan}</h1><p>Toplam Puan</p></div>", unsafe_allow_html=True)
    if st.button("♻️ Testi Sıfırla"):
        st.session_state.clear()
        st.rerun()

if not st.session_state.test_aktif:
    if st.button("🚀 Göreve Başla!"):
        st.session_state.test_sorulari = [yeni_nesil_soru_uret() for _ in range(10)]
        st.session_state.test_aktif = True
        st.session_state.soru_no = 0
        st.session_state.yanlislar = []
        st.session_state.zaman_baslangic = time.time()
        st.rerun()

elif st.session_state.soru_no < 10:
    soru = st.session_state.test_sorulari[st.session_state.soru_no]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div class='soru-box'><h3>Soru {st.session_state.soru_no + 1}</h3><p style='font-size:20px;'>{soru['s']}</p></div>", unsafe_allow_html=True)
        
        # index=None sayesinde hiçbir şık önceden seçili gelmez (Yusuf kendi seçmeli)
        cevap = st.radio("Cevabını Seç:", soru['siklar'], index=None, key=f"q_{st.session_state.soru_no}")
        
        if st.button("Onayla ve İlerle ➡️"):
            if cevap is None:
                st.warning("Lütfen bir şık seç Yusuf!")
            else:
                gecen_sure = time.time() - st.session_state.zaman_baslangic
                bonus = 5 if gecen_sure < 30 else 0
                
                if cevap == soru['c']:
                    st.session_state.puan += (10 + bonus)
                    st.toast(f"Tebrikler! +{10+bonus} Puan", icon="🔥")
                else:
                    st.session_state.yanlislar.append(soru)
                
                st.session_state.soru_no += 1
                st.session_state.zaman_baslangic = time.time()
                st.rerun()
    
    with col2:
        st.info(f"💡 Konu: {soru['tip']}")
        st.progress((st.session_state.soru_no + 1) * 10)

else:
    st.balloons()
    st.header("🏁 Görev Tamamlandı!")
    if st.session_state.yanlislar:
        st.subheader("🤖 Hata Analizi")
        for y in st.session_state.yanlislar:
            with st.expander(f"📍 {y['tip']} Çözümü"):
                st.write(f"**Soru:** {y['s']}")
                st.write(f"**Doğru Cevap:** {y['c']}")
                st.info(f"**Çözüm:** {y['analiz']}")
    
    if st.button("🔄 Yeni Görev"):
        st.session_state.test_aktif = False
        st.rerun()
