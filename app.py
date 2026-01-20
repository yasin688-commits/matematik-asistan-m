import streamlit as st
import random
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="Yusuf Agaç - Akıllı Matematik", page_icon="📐")

# Hafıza Yönetimi
if 'soru_tipi' not in st.session_state:
    st.session_state.soru_tipi = "Açılar"
if 'aktif_derece' not in st.session_state:
    st.session_state.aktif_derece = random.randint(10, 170)
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

# --- ÖZEL ÇİZİM FONKSİYONU (AÇILAR) ---
def aci_ciz(derece):
    import math
    rad = math.radians(derece)
    x = 100 + 80 * math.cos(-rad)
    y = 100 + 80 * math.sin(-rad)
    
    svg = f"""
    <svg width="200" height="200" viewBox="0 0 200 200" style="background-color: white; border-radius: 10px;">
        <line x1="100" y1="100" x2="180" y2="100" style="stroke:black;stroke-width:3" />
        <line x1="100" y1="100" x2="{x}" y2="{y}" style="stroke:red;stroke-width:3" />
        <circle cx="100" cy="100" r="5" fill="blue" />
        <text x="10" y="20" fill="black">Soru: Bu hangi açı?</text>
    </svg>
    """
    return svg

# --- TASARIM VE ASİSTAN ---
st.markdown("""
    <style>
    .asistan-kutusu { background-color: #e1f5fe; padding: 15px; border-radius: 15px; border-left: 5px solid #0288d1; margin: 10px 0; }
    .stButton>button { border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Yusuf Agaç: Matematik Asistanı")

# --- ASİSTAN BÖLÜMÜ ---
st.markdown(f"""
<div class="asistan-kutusu">
    <strong>🤖 Akıllı Asistan:</strong> Merhaba Yusuf! Bugün hangi konuyu fethedeceğiz? 
    Açıları mı yoksa problemleri mi?
</div>
""", unsafe_allow_html=True)

# --- SORU ALANI ---
tab1, tab2 = st.tabs(["📐 Açı Tanıma", "📝 Yeni Nesil Sorular"])

with tab1:
    st.header("Bu Açı Kaç Derece?")
    st.write("Aşağıdaki kırmızı çizginin oluşturduğu açıyı tahmin et.")
    
    st.markdown(aci_ciz(st.session_state.aktif_derece), unsafe_allow_html=True)
    
    tahmin = st.number_input("Tahminin (Derece):", key="aci_tahmin", step=1)
    
    if st.button("Kontrol Et (Açı)"):
        fark = abs(tahmin - st.session_state.aktif_derece)
        if fark <= 5: # 5 dereceye kadar yakınsa doğru kabul et
            st.balloons()
            st.success(f"Harikasın Yusuf! Tam olarak {st.session_state.aktif_derece}° idi.")
        else:
            st.error("Yanlış Cevap! Asistan yardımı geliyor...")
            with st.expander("🔍 Çözüm Animasyonu & Anlatımı"):
                st.write(f"Bak Yusuf, açıları ölçerken başlangıç çizgisinden (mavi nokta) ne kadar yukarı kalktığımıza bakarız.")
                st.write(f"1. Bu bir **{ 'DAR' if st.session_state.aktif_derece < 90 else 'GENİŞ' if st.session_state.aktif_derece > 90 else 'DİK'}** açıdır.")
                st.write(f"2. Doğru cevap: **{st.session_state.aktif_derece}°**")
                st.info("İpucu: Eğer dik olsaydı L harfi gibi görünürdü (90°).")

with tab2:
    st.header("Mantık Sorusu")
    s1 = random.randint(3, 8)
    s2 = random.randint(10, 20)
    soru = f"Yusuf her gün {s1} sayfa kitap okuyor. 10 gün sonra kitabın bitmesine {s2} sayfa kalıyor. Kitap toplam kaç sayfa?"
    dogru_cevap = (s1 * 10) + s2
    
    st.write(soru)
    cevap = st.number_input("Cevabın:", key="mantik_cevap", step=1)
    
    if st.button("Kontrol Et (Mantik)"):
        if cevap == dogru_cevap:
            st.success("Tebrikler Yusuf! Mantık kuralları senden sorulur. 🏆")
        else:
            st.error("Hatalı işlem! Asistan hemen açıklıyor:")
            st.markdown(f"""
            <div style="padding:10px; background:#fff3e0; border-radius:10px;">
                <strong>Adım Adım Çözüm:</strong><br>
                1. 10 günde okuduğun: {s1} sayfa x 10 gün = {s1*10} sayfa.<br>
                2. Kalan sayfa: {s2}.<br>
                3. Toplam: {s1*10} + {s2} = <b>{dogru_cevap}</b> sayfa.
            </div>
            """, unsafe_allow_html=True)

# Yeni Soru Butonu
if st.button("🔄 Yeni Soru Getir"):
    st.session_state.aktif_derece = random.randint(10, 170)
    st.rerun()
