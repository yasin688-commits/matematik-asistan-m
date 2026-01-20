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
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
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

# --- SORU MOTORU (YENİ NESİL) ---
def yeni_nesil_soru_uret():
    konu = random.choice(["Açılar", "Kesirler", "Market Problemi", "Zaman"])
    if konu == "Açılar":
        d = random.choice([30, 45, 60, 90, 120])
        return {
            "s": f"Yusuf bir pergel ile {d} derecelik bir açı çiziyor. Öğretmeni bu açıyı 'Doğru Açıya' (180°) tamamlamasını istiyor. Yusuf kaç derece daha çizmelidir?",
            "c": str(180-d), "siklar": [str(180-d), str(180-d-10), "90", "180"], "tip": "Açı",
            "analiz": f"Doğru açı 180 derecedir. 180 - {d} = {180-d} sonucuna ulaşırız."
        }
    elif konu == "Market Problemi":
        f = random.randint(5, 15)
        m = random.randint(3, 7)
        toplam = f * m
        return {
            "s": f"Yusuf tanesi {f} TL olan kalemlerden {m} tane alıyor. Kasaya 100 TL verirse ne kadar para üstü alır?",
            "c": str(100-toplam), "siklar": [str(100-toplam), str(toplam), str(100-toplam+5), "50"], "tip": "Problem",
            "analiz": f"Önce harcanan para: {f}x{m}={toplam} TL. Para üstü: 100-{toplam}={100-toplam} TL."
        }
    return {
        "s": "Bir günün 1/4'ünü uyuyarak geçiren Yusuf, kaç saat uyumuştur?",
        "c": "6", "siklar": ["6", "8", "4", "12"], "tip": "Zaman",
        "analiz": "Bir gün 24 saattir. 24'ün 1/4'ü 24/4 = 6 saattir."
    }

# --- YAN PANEL (VELİ VE KARNE) ---
with st.sidebar:
    rutbe, renk = rutbe_bul(st.session_state.puan)
    st.markdown(f"""<div class='rutbe-karti'><h3>{rutbe}</h3><h1 style='color:{renk};'>{st.session_state.puan}</h1><p>Toplam Puan</p></div>""", unsafe_allow_html=True)
    st.divider()
    if st.button("♻️ Testi Sıfırla"):
        st.session_state.clear()
        st.rerun()

# --- ANA EKRAN ---
st.title("🛡️ Yusuf'un Matematik Macera Üssü")

if not st.session_state.test_aktif:
    st.markdown("""
    ### Merhaba Yusuf! 👋
    Bugünkü görevine hazır mısın? 10 soruluk yeni bir görev seni bekliyor. 
    **Unutma:** Ne kadar hızlı ve doğru çözersen o kadar çok puan kazanırsın!
    """)
    if st.button("🚀 Göreve Başla!"):
        st.session_state.test_sorulari = [yeni_nesil_soru_uret() for _ in range(10)]
        st.session_state.test_aktif = True
        st.session_state.zaman_baslangic = time.time()
        st.rerun()

elif st.session_state.soru_no < 10:
    # --- SORU EKRANI ---
    soru = st.session_state.test_sorulari[st.session_state.soru_no]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div class='soru-box'><h3>Soru {st.session_state.soru_no + 1}</h3><p style='font-size:20px;'>{soru['s']}</p></div>", unsafe_allow_html=True)
        
        # Şıklar
        cevap = st.radio("Cevabını Seç:", soru['siklar'], key=f"q_{st.session_state.soru_no}")
        
        if st.button("Onayla ve İlerle ➡️"):
            # Süre bonusu kontrolü (İlk 30 saniyede ek puan)
            gecen_sure = time.time() - st.session_state.zaman_baslangic
            bonus = 5 if gecen_sure < 30 else 0
            
            if cevap == soru['c']:
                st.session_state.puan += (10 + bonus)
                st.toast(f"Mükemmel! +{10+bonus} Puan", icon="🔥")
            else:
                st.session_state.yanlislar.append(soru)
                st.toast("Sağlık olsun, öğrenmek için bir fırsat!", icon="💡")
            
            st.session_state.soru_no += 1
            st.session_state.zaman_baslangic = time.time() # Zamanı sıfırla
            st.rerun()
            
    with col2:
        st.info(f"💡 **İpucu:** {soru['tip']} konusundan bir soru çözüyorsun.")
        st.write("⏱️ **Zaman Bonusunu Kaçırma!**")
        st.progress(st.session_state.soru_no * 10)

else:
    # --- KARNE VE ANALİZ ---
    st.balloons()
    st.header("🏁 Görev Tamamlandı!")
    
    c1, c2 = st.columns(2)
    with c1:
        st.success(f"Yusuf, bu görevden toplam **{st.session_state.puan}** puana ulaştın!")
        if st.button("🔄 Yeni Görev Al"):
            st.session_state.test_aktif = False
            st.session_state.soru_no = 0
            st.rerun()
            
    with c2:
        if st.session_state.yanlislar:
            st.warning("🤖 Asistan Hata Analizi")
            for y in st.session_state.yanlislar:
                with st.expander(f"📍 {y['tip']} Sorusu Çözümü"):
                    st.write(f"**Soru:** {y['s']}")
                    st.write(f"**Doğru Cevap:** {y['c']}")
                    st.info(f"**Çözüm Yolu:** {y['analiz']}")
        else:
            st.success("HATA YOK! Sen tam bir şampiyonsun! 🏆")
