import streamlit as st
import random
import time
import pandas as pd

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Yusuf AI: Akıllı Akademi", page_icon="🧠", layout="wide")

# --- MODERN STİL TASARIMI ---
st.markdown("""
    <style>
    .stApp { background: #f8fafc; }
    .main-card { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-left: 8px solid #6366f1; }
    .stat-card { background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: white; padding: 20px; border-radius: 20px; text-align: center; }
    .question-text { font-size: 22px; font-weight: 600; color: #1e293b; margin-bottom: 20px; }
    .svg-container { background: #ffffff; border: 2px dashed #e2e8f0; border-radius: 20px; padding: 20px; margin: 15px 0; display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM HAFIZASI (SESSION STATE) ---
if 'gecmis_veriler' not in st.session_state: st.session_state.gecmis_veriler = []
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'test_aktif' not in st.session_state: st.session_state.test_aktif = False
if 'soru_no' not in st.session_state: st.session_state.soru_no = 0
if 'yanlislar' not in st.session_state: st.session_state.yanlislar = []
if 'secilen_sinif_hafiza' not in st.session_state: st.session_state.secilen_sinif_hafiza = "5. Sınıf"

# --- DİNAMİK GÖRSEL ÜRETİCİ (SVG) ---
def gorsel_ciz(tip):
    if tip == "Açı":
        return """<div class='svg-container'><svg width="200" height="100"><line x1="20" y1="80" x2="180" y2="80" stroke="#6366f1" stroke-width="4"/><line x1="20" y1="80" x2="100" y2="20" stroke="#f43f5e" stroke-width="4"/><path d="M 50 80 A 30 30 0 0 1 40 65" fill="none" stroke="#f59e0b" stroke-width="3"/></svg></div>"""
    if tip == "Kesir":
        return """<div class='svg-container'><svg width="120" height="120"><circle cx="60" cy="60" r="50" fill="none" stroke="#6366f1" stroke-width="2"/><path d="M 60 60 L 60 10 A 50 50 0 0 1 110 60 Z" fill="#a855f7" opacity="0.6"/></svg></div>"""
    return """<div class='svg-container'><svg width="100" height="100"><rect x="20" y="20" width="60" height="60" rx="10" fill="#6366f1" opacity="0.2" stroke="#6366f1" stroke-width="2"/></svg></div>"""

# --- YENİ NESİL SORU MOTORU ---
def yeni_nesil_soru_uret(sinif_no, ders, zorluk):
    s_id = random.randint(1000, 9999)
    # Sınıf bazlı zorluk katsayısı
    k = sinif_no * 2
    
    if ders == "Matematik":
        if sinif_no <= 4:
            a, b = random.randint(10, 50), random.randint(5, 20)
            return {
                "id": s_id, "s": f"Yusuf'un {a} misketi var. Arkadaşı Kerem ona {b} misket daha veriyor. Yusuf misketlerini 3 kutuya eşit paylaştırırsa her kutuda kaç misket olur?",
                "c": str((a+b)//3), "siklar": [str((a+b)//3), str(a+b), str(a-b), "15"], "konu": "Problem", "g": "Kutu",
                "analiz": f"Önce toplamı buluruz ({a}+{b}={a+b}), sonra 3'e böleriz."
            }
        elif sinif_no <= 8:
            d = random.choice([30, 45, 60])
            return {
                "id": s_id, "s": f"Bir doğru açı üzerinde bulunan üç açıdan ikisinin ölçüsü {d} ve {d+20} derecedir. Yusuf kalan üçüncü açıyı kaç derece ölçmelidir?",
                "c": str(180 - (d + d + 20)), "siklar": [str(180-(2*d+20)), "90", "180", str(d)], "konu": "Açılar", "g": "Açı",
                "analiz": "Doğru açı 180 derecedir. Bilinenleri toplayıp 180'den çıkarırız."
            }
    # Fen ve Türkçe için benzer dinamik yapılar...
    return {
        "id": s_id, "s": f"{sinif_no}. Sınıf için genel yetenek sorusu: Hangisi canlıların temel yapı taşıdır?",
        "c": "Hücre", "siklar": ["Hücre", "Atom", "Molekül", "Organ"], "konu": "Biyoloji", "g": "Genel",
        "analiz": "Tüm canlılar hücrelerden oluşur."
    }

# --- ANALİZ MERKEZİ ---
def zayif_nokta_bul():
    if not st.session_state.gecmis_veriler: return "Genel", 0
    df = pd.DataFrame(st.session_state.gecmis_veriler)
    yanlislar = df[df['durum'] == 'Yanlış']
    if yanlislar.empty: return "Yok (Harikasın!)", 0
    return yanlislar['konu'].value_counts().idxmax(), len(yanlislar)

# --- ARAYÜZ ---
st.sidebar.markdown(f"<div class='stat-card'><h3>🏆 {st.session_state.puan} Puan</h3></div>", unsafe_allow_html=True)
z_konu, z_sayi = zayif_nokta_bul()
st.sidebar.warning(f"📉 En Çok Hata Yapılan: {z_konu}")

if not st.session_state.test_aktif:
    st.title("🚀 Yusuf Learning Hub: Başarı Odası")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    s_secim = c1.selectbox("Sınıf Seviyen:", [f"{i}. Sınıf" for i in range(1, 13)], index=4)
    st.session_state.secilen_sinif_hafiza = s_secim # Hata düzeltme kaydı
    d_secim = c2.selectbox("Ders Seç:", ["Matematik", "Fen Bilimleri", "Türkçe"])
    z_secim = c3.select_slider("Zorluk:", ["Kolay", "Orta", "Zor"])
    
    if st.button("Eğitime Başla ⚡"):
        sinif_int = int(s_secim.split('.')[0])
        st.session_state.test_sorulari = [yeni_nesil_soru_uret(sinif_int, d_secim, z_secim) for _ in range(5)]
        st.session_state.test_aktif = True
        st.session_state.soru_no = 0
        st.session_state.yanlislar = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.soru_no < len(st.session_state.test_sorulari):
    soru = st.session_state.test_sorulari[st.session_state.soru_no]
    st.progress((st.session_state.soru_no + 1) * 20)
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown(f"**SORU {st.session_state.soru_no + 1}** | {soru['konu']}")
    st.markdown(gorsel_ciz(soru['g']), unsafe_allow_html=True)
    st.markdown(f"<p class='question-text'>{soru['s']}</p>", unsafe_allow_html=True)
    
    cevap = st.radio("Cevabını seç Yusuf:", soru['siklar'], index=None, key=f"q_{soru['id']}")
    
    col_a, col_b = st.columns(2)
    if col_a.button("Cevabı Onayla ➡️"):
        if cevap:
            durum = "Doğru" if cevap == soru['c'] else "Yanlış"
            p_ekle = 20 if durum == "Doğru" else 0
            
            # Kalıcı Kayıt (Hata düzeltilmiş kısım)
            st.session_state.gecmis_veriler.append({
                "sinif": st.session_state.secilen_sinif_hafiza,
                "konu": soru['konu'],
                "durum": durum,
                "tarih": time.strftime("%H:%M")
            })
            
            if durum == "Yanlış": st.session_state.yanlislar.append(soru)
            st.session_state.puan += p_ekle
            st.session_state.soru_no += 1
            st.rerun()
        else: st.warning("Lütfen seçim yap!")
    
    if col_b.button("🛑 Testi Bitir"):
        st.session_state.soru_no = 99
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.balloons()
    st.header("🏁 Görev Tamamlandı!")
    if st.session_state.yanlislar:
        st.subheader("🤖 Akıllı Çözüm Rehberi")
        for y in st.session_state.yanlislar:
            with st.expander(f"❌ {y['s'][:60]}..."):
                st.markdown(gorsel_ciz(y['g']), unsafe_allow_html=True)
                st.write(f"**Doğru Cevap:** {y['c']}")
                st.info(f"**Nasıl Çözülür?** {y['analiz']}")
                if st.button(f"'{y['konu']}' İçin Benzer Soru Üret", key=f"b_{y['id']}"):
                    st.write("Yusuf, bu konudan 5 tane benzer soru çalışma kağıdına eklendi!")

    if st.button("Ana Sayfaya Dön"):
        st.session_state.test_aktif = False
        st.rerun()
