import streamlit as st
import random
import time

# --- SAYFA YAPILANDIRMASI VE MODERN TEMA ---
st.set_page_config(page_title="Yusuf AI Learning Hub", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #f8f9fa; }
    .main-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-top: 5px solid #6c5ce7; }
    .stat-card { background: #6c5ce7; color: white; padding: 15px; border-radius: 15px; text-align: center; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3em; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background: #a29bfe; color: white; transform: translateY(-2px); }
    .svg-container { text-align: center; background: #fdfdfd; padding: 20px; border-radius: 15px; margin: 10px 0; border: 1px dashed #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM HAFIZASI ---
if 'puan' not in st.session_state: st.session_state.puan = 0
if 'test_aktif' not in st.session_state: st.session_state.test_aktif = False
if 'soru_no' not in st.session_state: st.session_state.soru_no = 0
if 'yanlislar' not in st.session_state: st.session_state.yanlislar = []
if 'mevcut_soru' not in st.session_state: st.session_state.mevcut_soru = None

# --- GÖRSEL ÜRETİCİ (SVG) ---
def gorsel_hazirla(tip):
    if tip == "Geometri":
        return """<div class='svg-container'><svg width="200" height="120"><rect x="50" y="20" width="100" height="80" fill="#e1f5fe" stroke="#01579b" stroke-width="3"/><text x="75" y="115" font-size="12">Bahçe Planı</text></svg></div>"""
    elif tip == "Alışveriş":
        return """<div class='svg-container'><svg width="200" height="120"><circle cx="60" cy="60" r="30" fill="#fff9c4" stroke="#fbc02d"/><circle cx="140" cy="60" r="30" fill="#fff9c4" stroke="#fbc02d"/><text x="80" y="110" font-size="12">Ürün Paketleri</text></svg></div>"""
    return """<div class='svg-container'><svg width="200" height="100"><line x1="20" y1="80" x2="180" y2="80" stroke="black" stroke-width="2"/><path d="M 50 80 A 50 50 0 0 1 150 80" fill="none" stroke="red" stroke-width="2"/></svg></div>"""

# --- YENİ NESİL SORU MOTORU ---
def yeni_nesil_uret(sinif, ders, zorluk):
    s_id = random.randint(100, 999)
    # 5. Sınıf Matematik Örneği (Senaryolu)
    if sinif <= 6:
        a = random.randint(10, 50)
        b = random.randint(5, 15)
        toplam = a * b
        return {
            "id": s_id,
            "soru": f"Yusuf, okul kütüphanesi için her birinde {a} kitap bulunan {b} tane koli hazırlıyor. Kütüphaneci Yusuf'a toplam kitap sayısını soruyor. Yusuf'un vermesi gereken cevap nedir?",
            "cevap": str(toplam),
            "siklar": [str(toplam), str(toplam-a), str(toplam+10), str(a+b)],
            "analiz": f"Koli sayısı ile koli içindeki kitap sayısını çarpmalıyız: {a} x {b} = {toplam}.",
            "gorsel": "Alışveriş",
            "tip": "Matematik"
        }
    else: # Lise Seviyesi
        return {
            "id": s_id,
            "soru": "Bir laboratuvarda bakteri popülasyonu her saat başı 2 katına çıkmaktadır. Başlangıçta 100 bakteri varsa, 3 saat sonra kaç bakteri olur?",
            "cevap": "800",
            "siklar": ["800", "400", "600", "1600"],
            "analiz": "1. saat: 200, 2. saat: 400, 3. saat: 800 olur (2^3 x 100).",
            "gorsel": "Geometri",
            "tip": "Fen/Matematik"
        }

# --- ARAYÜZ TASARIMI ---
st.title("🛡️ Yusuf Agaç Learning Hub v8.0")

# Sol Panel: Durum
with st.sidebar:
    st.markdown(f"<div class='stat-card'><h3>🏆 PUAN: {st.session_state.puan}</h3></div>", unsafe_allow_html=True)
    st.divider()
    if st.button("🚪 Testi Bitir ve Çık"):
        st.session_state.soru_no = 10
        st.rerun()

# Ana Ekran
if not st.session_state.test_aktif:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("🚀 Eğitim Ayarlarını Yap")
    c1, c2, c3 = st.columns(3)
    secilen_sinif = c1.selectbox("Sınıfın:", [f"{i}. Sınıf" for i in range(1, 13)], index=4)
    secilen_ders = c2.selectbox("Dersin:", ["Matematik", "Fen Bilimleri", "Türkçe"])
    secilen_zorluk = c3.select_slider("Zorluk:", ["Kolay", "Orta", "Zor"])
    
    if st.button("Görevi Başlat ⚡"):
        st.session_state.test_sorulari = [yeni_nesil_uret(int(secilen_sinif.split('.')[0]), secilen_ders, secilen_zorluk) for _ in range(10)]
        st.session_state.test_aktif = True
        st.session_state.soru_no = 0
        st.session_state.yanlislar = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.soru_no < 10:
    # Soru Ekranı
    soru = st.session_state.test_sorulari[st.session_state.soru_no]
    st.progress((st.session_state.soru_no + 1) * 10)
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.write(f"**GÖREV {st.session_state.soru_no + 1}/10**")
    
    # Görsel Eklenmesi
    st.markdown(gorsel_hazirla(soru['gorsel']), unsafe_allow_html=True)
    
    st.subheader(soru['soru'])
    secim = st.radio("Seçeneğini işaretle:", soru['siklar'], index=None, key=f"r_{soru['id']}")
    
    col1, col2 = st.columns(2)
    if col1.button("Onayla ve Devam Et"):
        if secim:
            if secim == soru['cevap']:
                st.session_state.puan += 20
                st.toast("Mükemmel! +20 Puan", icon="🔥")
            else:
                st.session_state.yanlislar.append(soru)
                st.toast("Not alındı, sonra inceleyeceğiz.", icon="📌")
            st.session_state.soru_no += 1
            st.rerun()
        else:
            st.warning("Bir şık seçmelisin Yusuf!")
    
    if col2.button("⚠️ Bu Soru Zor, Benzerini Göster"):
        st.info("Asistan senin için benzer bir mantık sorusu hazırlıyor...")
        time.sleep(1)
        st.session_state.test_sorulari[st.session_state.soru_no] = yeni_nesil_uret(5, "Matematik", "Orta")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Sonuç ve Analiz
    st.balloons()
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.header("🏁 Görev Analiz Raporu")
    st.write(f"Tebrikler Yusuf! Toplam {st.session_state.puan} puan kazandın.")
    
    if st.session_state.yanlislar:
        st.subheader("🤖 Yapay Zeka Hata Analiz ve Çözüm")
        for y in st.session_state.yanlislar:
            with st.expander(f"❌ {y['soru'][:50]}..."):
                st.markdown(gorsel_hazirla(y['gorsel']), unsafe_allow_html=True)
                st.write(f"**Doğru Cevap:** {y['cevap']}")
                st.info(f"**Asistan Çözümü:** {y['analiz']}")
                if st.button(f"Bu Soru Tipinden 5 Tane Daha Üret", key=f"extra_{y['id']}"):
                    st.write("Yeni çalışma kağıdı hazırlanıyor...")
    
    if st.button("Yeni Maceraya Başla 🔄"):
        st.session_state.test_aktif = False
        st.session_state.puan = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
