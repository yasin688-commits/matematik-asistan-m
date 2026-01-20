import streamlit as st
import random
import time
import pandas as pd # İstatistikler için

# --- MODERN TASARIM VE STİL ---
st.set_page_config(page_title="Yusuf AI: Akıllı Koç", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #f4f7f6; }
    .stat-box { background: white; padding: 20px; border-radius: 15px; border-bottom: 5px solid #6c5ce7; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .highlight { color: #6c5ce7; font-weight: bold; }
    .card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- KALICI HAFIZA YÖNETİMİ ---
# Not: Gerçek bir veritabanı yerine session_state kullanıyoruz, 
# ancak bu yapı bir sonraki aşamada kolayca Google Sheets'e bağlanabilir.
if 'gecmis_veriler' not in st.session_state:
    st.session_state.gecmis_veriler = [] # Yusuf'un tüm geçmiş çözümleri
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'test_aktif' not in st.session_state: st.session_state.test_aktif = False
if 'soru_no' not in st.session_state: st.session_state.soru_no = 0

# --- ANALİZ VE KONU ÖNERİ SİSTEMİ ---
def eksik_konu_analizi():
    if not st.session_state.gecmis_veriler:
        return "Genel"
    
    df = pd.DataFrame(st.session_state.gecmis_veriler)
    # Sadece yanlışları filtrele
    yanlislar = df[df['durum'] == 'Yanlış']
    
    if yanlislar.empty:
        return "Genel"
    
    # En çok yanlış yapılan konuyu bul
    en_cok_yanlis = yanlislar['konu'].value_counts().idxmax()
    return en_cok_yanlis

# --- YENİ NESİL DİNAMİK SORU ÜRETİCİ ---
def soru_uret(konu_odagi="Genel"):
    konular = ["Açılar", "Kesirler", "Doğal Sayılar", "Geometri", "Mantık"]
    secilen_konu = konu_odagi if konu_odagi != "Genel" else random.choice(konular)
    
    s_id = random.randint(1000, 9999)
    a, b = random.randint(10, 50), random.randint(2, 10)
    
    # Yeni Nesil Senaryolar
    senaryolar = {
        "Açılar": {
            "s": f"Yusuf bir kağıda {a*2} derecelik bir açı çiziyor. Bu açıyı dik açıya (90°) tamamlamak için kaç derece daha eklemelidir?",
            "c": str(90 - (a*2) if 90 > a*2 else 180 - (a*2)),
            "analiz": "Dik açı 90 derecedir. Aradaki farkı bulmalısın."
        },
        "Doğal Sayılar": {
            "s": f"Yusuf'un kumbarasında her gün {b} TL birikiyor. {a} gün sonra toplam parasını hesaplayan Yusuf, 50 TL'ye bir kitap almak istiyor. Kaç TL'si kalır?",
            "c": str((a*b) - 50),
            "analiz": f"Önce toplam parayı bul ({a}x{b}), sonra 50 TL çıkart."
        },
        "Kesirler": {
            "s": f"Yusuf 120 sayfalık kitabın 1/{b if b > 0 else 2}'ini okudu. Geriye okunacak kaç sayfası kaldı?",
            "c": str(120 - (120 // (b if b > 0 else 2))),
            "analiz": "Önce okunan sayfayı bulup bütünden çıkartmalısın."
        }
    }
    
    # Eğer konu senaryoda yoksa varsayılan getir
    data = senaryolar.get(secilen_konu, senaryolar["Doğal Sayılar"])
    
    dogru = data["c"]
    siklar = [dogru, str(int(dogru)+10), str(int(dogru)-5), "0"]
    random.shuffle(siklar)
    
    return {"id": s_id, "soru": data["s"], "cevap": dogru, "siklar": siklar, "konu": secilen_konu, "analiz": data["analiz"]}

# --- ARAYÜZ ---
st.title("🧠 Yusuf AI: Kişiselleştirilmiş Öğrenme Asistanı")

# Üst Bilgi Paneli (İstatistikler)
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1:
    st.markdown(f"<div class='stat-box'>🏁 Toplam Soru<br><h2>{len(st.session_state.gecmis_veriler)}</h2></div>", unsafe_allow_html=True)
with col_stat2:
    eksik = eksik_konu_analizi()
    st.markdown(f"<div class='stat-box'>📉 En Çok Yanlış Yapılan<br><h2 style='color:red;'>{eksik}</h2></div>", unsafe_allow_html=True)
with col_stat3:
    st.markdown(f"<div class='stat-box'>⭐ Toplam Puan<br><h2 style='color:green;'>{st.session_state.puan}</h2></div>", unsafe_allow_html=True)

st.divider()

if not st.session_state.test_aktif:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎯 Yusuf, Bugün Ne Yapıyoruz?")
    
    tab1, tab2 = st.tabs(["🚀 Yeni Görev", "📊 Gelişim Raporu"])
    
    with tab1:
        st.write(f"Sistem analizi yapıldı: **{eksik}** konusuna ağırlık vermen öneriliyor.")
        mode = st.radio("Test Modu:", ["Karışık (Normal)", f"Akıllı Odak ({eksik})"])
        
        if st.button("Eğitimi Başlat"):
            odak = eksik if "Akıllı Odak" in mode else "Genel"
            st.session_state.test_sorulari = [soru_uret(odak) for _ in range(5)]
            st.session_state.test_aktif = True
            st.session_state.soru_no = 0
            st.rerun()
            
    with tab2:
        if st.session_state.gecmis_veriler:
            df_hist = pd.DataFrame(st.session_state.gecmis_veriler)
            st.dataframe(df_hist, use_container_width=True)
            st.line_chart(df_hist['puan_degisimi'].cumsum())
        else:
            st.info("Henüz veri toplanmadı. Birkaç test çözerek başlayabilirsin!")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.soru_no < len(st.session_state.test_sorulari):
    # SORU EKRANI
    soru = st.session_state.test_sorulari[st.session_state.soru_no]
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.caption(f"📍 Konu: {soru['konu']} | Soru {st.session_state.soru_no + 1}")
    st.subheader(soru['soru'])
    
    secim = st.radio("Cevabın:", soru['siklar'], index=None, key=f"q_{soru['id']}")
    
    col_c1, col_c2 = st.columns(2)
    if col_c1.button("Onayla ve İlerle"):
        if secim:
            durum = "Doğru" if secim == soru['cevap'] else "Yanlış"
            puan_ekle = 20 if durum == "Doğru" else 0
            
            # HAFIZAYA KAYDET
            st.session_state.gecmis_veriler.append({
                "soru": soru['soru'],
                "konu": soru['konu'],
                "durum": durum,
                "puan_degisimi": puan_ekle,
                "tarih": time.strftime("%H:%M:%S")
            })
            
            st.session_state.puan += puan_ekle
            st.session_state.soru_no += 1
            st.rerun()
        else:
            st.warning("Seçim yapmalısın!")
            
    if col_c2.button("🛑 Testi Bitir ve Analiz Et"):
        st.session_state.soru_no = 100 # Testi sonlandır
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # ANALİZ EKRANI
    st.success("Test Tamamlandı! Asistan verileri işledi.")
    if st.button("Sonuçları Gör ve Ana Menüye Dön"):
        st.session_state.test_aktif = False
        st.rerun()
