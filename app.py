import streamlit as st
import random
import time
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Yusuf AI: Master Akademi", page_icon="🎓", layout="wide")

# --- MODERN VE EĞLENCELİ TASARIM ---
st.markdown("""
    <style>
    .stApp { background: #f0f4f8; }
    .main-card { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border-top: 10px solid #4f46e5; }
    .report-card { background: #ffffff; padding: 20px; border-radius: 20px; border-left: 5px solid #ef4444; margin-top: 10px; }
    .stButton>button { border-radius: 15px; height: 3.5em; background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%); color: white; border: none; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(79, 70, 229, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- KALICI HAFIZA SİSTEMİ ---
if 'hafiza' not in st.session_state:
    st.session_state.hafiza = [] # Yusuf'un tüm geçmişi buraya kaydedilir
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'test_aktif' not in st.session_state: st.session_state.test_aktif = False

# --- YENİ NESİL SORU MOTORU (RESİMDEKİ SORU TİPLERİ EKLENDİ) ---
def soru_motoru(sinif, konu_odagi=None):
    s_id = random.randint(10000, 99999)
    # Yusuf'un resminden ilham alan soru tipleri
    tipler = ["Yol Problemi", "Basamak Değeri", "Örüntü", "Mantık Muhakeme", "Saat ve Açı"]
    secilen_tip = konu_odagi if konu_odagi else random.choice(tipler)
    
    if secilen_tip == "Yol Problemi":
        toplam_yol = random.choice([48, 72, 96, 120])
        s = f"Yusuf, A şehrinden H şehrine giderken yolun yarısında mola veriyor. {toplam_yol//4} km daha giderse yolun çeyreği kalıyor. Tüm yol kaç km'dir?"
        c = str(toplam_yol)
        analiz = "Yolun yarısı ile çeyreği arasındaki fark toplam yolun 1/4'üdür."
        g = "yol"
    elif secilen_tip == "Basamak Değeri":
        a = random.randint(1000, 9000)
        s = f"A = Yüzler basamağındaki rakamı 6 olan dört basamaklı en küçük sayı. B = Onlar basamağındaki rakamı 2 olan dört basamaklı en büyük sayı. B - A kaçtır?"
        c = str(9929 - 1600)
        analiz = "En büyük için diğer basamaklara 9, en küçük için en küçük rakamları koymalısın."
        g = "sayi"
    elif secilen_tip == "Örüntü":
        baslangic = random.randint(5, 15)
        artis = random.randint(4, 7)
        s = f"{baslangic} - {baslangic+artis} - {baslangic+2*artis} - ... örüntüsünde 7. adımda hangi sayı yazılır?"
        c = str(baslangic + (6 * artis))
        analiz = "n. adım formülü: Başlangıç + (Adım Sayısı - 1) x Artış Miktarı"
        g = "sayi"
    else:
        s = "Bir saatte akrep ile yelkovan tam 15:00'i gösterirken aralarındaki açı kaç derecedir?"
        c = "90"
        analiz = "Saat 15:00'te yelkovan 12, akrep 3 üzerindedir. Bu tam bir dik açıdır (90 derece)."
        g = "saat"

    # KeyError Hatalarını önlemek için güvenli sözlük yapısı
    return {
        "id": s_id, "soru": s, "cevap": c, 
        "siklar": random.sample([c, str(int(c)+10), str(int(c)-15), str(int(c)+25)], 4) if c.isdigit() else [c, "A", "B", "C"],
        "analiz": analiz, "konu": secilen_tip, "gorsel_tip": g
    }

# --- AKILLI RAPORLAMA ---
def rapor_olustur():
    if not st.session_state.hafiza: return None
    df = pd.DataFrame(st.session_state.hafiza)
    rapor = df.groupby('konu')['durum'].value_counts().unstack().fillna(0)
    if 'Yanlış' not in rapor: rapor['Yanlış'] = 0
    eksik_konular = rapor[rapor['Yanlış'] > 0].index.tolist()
    return eksik_konular

# --- ARAYÜZ ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3426/3426652.png", width=100)
st.sidebar.title(f"Yusuf'un Puanı: {st.session_state.puan}")

if not st.session_state.test_aktif:
    st.title("🛡️ Yusuf AI: Geleceğin Bilgini")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🚀 Teste Başla", "📊 AI Gelişim Raporu"])
    
    with tab1:
        c1, c2 = st.columns(2)
        sinif = c1.selectbox("Sınıfın", ["5. Sınıf", "6. Sınıf", "7. Sınıf"], index=0)
        eksikler = rapor_olustur()
        
        if eksikler:
            st.warning(f"🚨 Yapay Zeka Analizi: **{', '.join(eksikler)}** konularında desteğe ihtiyacın var!")
            mod = st.toggle("Yapay Zeka Destekli Mod (Eksik Konulara Odaklan)")
        else:
            mod = False
            
        if st.button("Macerayı Başlat!"):
            odak = random.choice(eksikler) if (mod and eksikler) else None
            st.session_state.sorular = [soru_motoru(sinif, odak) for _ in range(5)]
            st.session_state.test_aktif = True
            st.session_state.soru_no = 0
            st.session_state.yanlis_listesi = []
            st.rerun()

    with tab2:
        if st.session_state.hafiza:
            st.write("Son 10 sorudaki performansın:")
            df_h = pd.DataFrame(st.session_state.hafiza).tail(10)
            st.table(df_h[['konu', 'durum']])
        else:
            st.info("Henüz rapor oluşturacak kadar soru çözmedin Yusuf!")
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.soru_no < len(st.session_state.sorular):
    soru = st.session_state.sorular[st.session_state.soru_no]
    st.progress((st.session_state.soru_no + 1) * 20)
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.caption(f"📍 Konu: {soru['konu']}")
    st.subheader(soru['soru'])
    
    secim = st.radio("Cevabın:", soru['siklar'], index=None, key=f"s_{soru['id']}")
    
    if st.button("Onayla"):
        if secim:
            durum = "Doğru" if secim == soru['cevap'] else "Yanlış"
            if durum == "Doğru": st.session_state.puan += 20
            else: st.session_state.yanlis_listesi.append(soru)
            
            # HAFIZAYA KAYDET
            st.session_state.hafiza.append({"konu": soru['konu'], "durum": durum, "tarih": time.strftime("%H:%M")})
            
            st.session_state.soru_no += 1
            st.rerun()
        else:
            st.error("Lütfen bir şık seç!")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.balloons()
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.header("🏁 Test Bitti!")
    
    if st.session_state.yanlis_listesi:
        st.subheader("🤖 Yapay Zeka Hata Analizi")
        for y in st.session_state.yanlis_listesi:
            st.markdown(f"""
            <div class='report-card'>
                <b>Soru:</b> {y['soru']}<br>
                <span style='color:green;'><b>Doğru Cevap:</b> {y['cevap']}</span><br>
                <span style='color:blue;'><b>Çözüm Yolu:</b> {y['analiz']}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Bu Konudan ({y['konu']}) Benzer Soru Üret", key=f"b_{y['id']}"):
                st.info("Asistan senin için benzer soruları hazırlıyor...")
    
    if st.button("Ana Menüye Dön"):
        st.session_state.test_aktif = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
