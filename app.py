import streamlit as st
import random
import time
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Yusuf AI: Tam Kapsamlı Akademi", page_icon="🎓", layout="wide")

# --- MODER TASARIM ---
st.markdown("""
    <style>
    .stApp { background: #f0f2f5; }
    .main-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.05); }
    .sidebar-stat { background: #6c5ce7; color: white; padding: 15px; border-radius: 12px; margin-bottom: 10px; text-align: center; }
    .correct-anim { color: #00b894; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM HAFIZASI (UNUTMAZ) ---
if 'gecmis_veriler' not in st.session_state: st.session_state.gecmis_veriler = []
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'test_aktif' not in st.session_state: st.session_state.test_aktif = False
if 'soru_no' not in st.session_state: st.session_state.soru_no = 0
if 'yanlislar' not in st.session_state: st.session_state.yanlislar = []

# --- AKILLI ANALİZ FONKSİYONU ---
def analiz_et():
    if not st.session_state.gecmis_veriler:
        return "Henüz veri yok", "Genel"
    df = pd.DataFrame(st.session_state.gecmis_veriler)
    yanlis_df = df[df['durum'] == 'Yanlış']
    if yanlis_df.empty:
        return "Harika gidiyorsun!", "Genel"
    en_zayif_konu = yanlis_df['konu'].value_counts().idxmax()
    return f"Dikkat: {en_zayif_konu} konusuna odaklanmalısın.", en_zayif_konu

# --- YENİ NESİL SORU MOTORU (SINIF VE DERS BAZLI) ---
def yeni_nesil_soru_uret(sinif, ders, zorluk, odak_konu=None):
    # Sınıf bazlı sayısal zorluk ayarı
    carpan = sinif * 10
    a, b = random.randint(1, carpan), random.randint(1, carpan)
    
    # Soru Havuzu Mantığı
    if ders == "Matematik":
        if sinif <= 4:
            s = f"Yusuf'un {a} elması vardı. Arkadaşı ona {b} elma daha verdi. Yusuf'un toplam kaç elması oldu?"
            c = str(a + b)
            analiz = f"{a} + {b} = {c} eder. Toplama işlemi bütünü artırır."
            konu = "Toplama"
        elif sinif <= 8:
            d = random.choice([30, 45, 60, 90])
            s = f"Bir ABC üçgeninde iki iç açının toplamı {d + 20} derecedir. Üçüncü açıyı bulmak isteyen Yusuf'a yardım et."
            c = str(180 - (d + 20))
            analiz = "Üçgenin iç açıları toplamı 180 derecedir. 180 - (bilinen açılar) = sonuç."
            konu = "Açılar"
        else:
            s = f"f(x) = {sinif}x + {a} fonksiyonunda x=2 için sonuç nedir?"
            c = str(sinif * 2 + a)
            analiz = "Fonksiyonda x gördüğün yere 2 yazıp işlemi yapmalısın."
            konu = "Fonksiyonlar"
    elif ders == "Fen Bilimleri":
        s = "Dünya'nın kendi ekseni etrafında dönmesiyle ne oluşur?"
        c = "Gece ve Gündüz"
        analiz = "Dünya 24 saatte bir turunu tamamlar ve gece-gündüz döngüsü oluşur."
        konu = "Dünya ve Evren"
    else:
        s = "Aşağıdaki cümlelerin hangisinde bir yazım yanlışı vardır?"
        c = "Yusuf'da gelicek."
        analiz = "Bağlaç olan 'da' ayrı yazılmalıdır: 'Yusuf da gelecek'."
        konu = "Yazım Kuralları"

    siklar = [c, str(int(c)+5) if c.isdigit() else "Yanlış Şık 1", 
              str(int(c)-2) if c.isdigit() else "Yanlış Şık 2", "Hiçbiri"]
    random.shuffle(siklar)
    return {"soru": s, "cevap": c, "siklar": siklar, "analiz": analiz, "konu": konu, "ders": ders}

# --- ARAYÜZ ---
with st.sidebar:
    st.markdown(f"<div class='sidebar-stat'><h3>⭐ PUAN: {st.session_state.puan}</h3></div>", unsafe_allow_html=True)
    mesaj, zayif_konu = analiz_et()
    st.warning(mesaj)
    st.divider()
    if st.button("🗑️ Tüm Hafızayı Sil"):
        st.session_state.clear()
        st.rerun()

st.title("🛡️ Yusuf AI Learning Hub v10.0")

if not st.session_state.test_aktif:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Eğitim Ayarlarını Yap")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        s_secim = st.selectbox("Sınıf Seç:", [f"{i}. Sınıf" for i in range(1, 13)], index=4)
        sinif_num = int(s_secim.split('.')[0])
    with c2:
        d_secim = st.selectbox("Ders Seç:", ["Matematik", "Fen Bilimleri", "Türkçe"])
    with c3:
        z_secim = st.select_slider("Zorluk:", ["Kolay", "Orta", "Zor"])
        
    mode = st.radio("Soru Üretim Modu:", ["Müfredata Göre (Normal)", f"Hafıza Odaklı (Zayıf Konun: {zayif_konu})"])
    
    if st.button("Macerayı Başlat 🚀"):
        st.session_state.test_sorulari = [yeni_nesil_soru_uret(sinif_num, d_secim, z_secim) for _ in range(5)]
        st.session_state.test_aktif = True
        st.session_state.soru_no = 0
        st.session_state.yanlislar = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.soru_no < len(st.session_state.test_sorulari):
    # SORU EKRANI
    soru = st.session_state.test_sorulari[st.session_state.soru_no]
    st.progress((st.session_state.soru_no + 1) * 20)
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.caption(f"📍 {soru['ders']} | {soru['konu']}")
    st.subheader(soru['soru'])
    
    # SVG GÖRSEL (Temsili)
    st.write("---")
    
    cevap = st.radio("Seçeneğin:", soru['siklar'], index=None, key=f"q_{st.session_state.soru_no}")
    
    col_a, col_b = st.columns(2)
    if col_a.button("Onayla ve Devam Et"):
        if cevap:
            durum = "Doğru" if cevap == soru['cevap'] else "Yanlış"
            p_degisim = 20 if durum == "Doğru" else 0
            
            # HAFIZAYA KAYDET (Gelecek analizler için)
            st.session_state.gecmis_veriler.append({
                "sinif": s_secim, "ders": soru['ders'], "konu": soru['konu'],
                "durum": durum, "puan_katkisi": p_degisim, "tarih": time.strftime("%D %H:%M")
            })
            
            if durum == "Yanlış": st.session_state.yanlislar.append(soru)
            st.session_state.puan += p_degisim
            st.session_state.soru_no += 1
            st.rerun()
        else:
            st.warning("Lütfen bir cevap seç Yusuf!")
            
    if col_b.button("🛑 Testi Yarıda Kes"):
        st.session_state.soru_no = 99
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # SONUÇ EKRANI
    st.balloons()
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.header("📊 Görev Raporu")
    st.write(f"Bu testten toplam {st.session_state.puan} puana ulaştın.")
    
    if st.session_state.yanlislar:
        st.subheader("🤖 Yanlışların Çözümü (Öğrenme Zamanı)")
        for y in st.session_state.yanlislar:
            with st.expander(f"❌ {y['soru'][:50]}..."):
                st.write(f"**Doğru Cevap:** {y['cevap']}")
                st.info(f"**Asistan Açıklaması:** {y['analiz']}")
                if st.button(f"'{y['konu']}' Konusundan Benzer Soru Üret", key=f"btn_{random.random()}"):
                    st.write("Bu konu üzerinde daha fazla çalışmak harika bir fikir!")
    
    if st.button("Ana Menüye Dön"):
        st.session_state.test_aktif = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
