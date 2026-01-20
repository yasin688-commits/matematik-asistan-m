import streamlit as st
import random
import math

# Sayfa Yapılandırması
st.set_page_config(page_title="Yusuf Agaç - Modern Matematik", page_icon="📐")

# Hafıza Yönetimi
if 'dogru_cevap' not in st.session_state:
    st.session_state.dogru_cevap = ""
if 'aci_degeri' not in st.session_state:
    st.session_state.aci_degeri = 90

# --- YENİ NESİL AÇI ÇİZİCİ ---
def modern_aci_ciz(derece):
    rad = math.radians(derece)
    # Merkeze göre koordinatlar (Daha net bir görünüm için)
    x = 150 + 100 * math.cos(-rad)
    y = 150 + 100 * math.sin(-rad)
    
    # Açı türüne göre renk belirle
    renk = "#FF4B4B" if derece < 90 else "#32CD32" if derece > 90 else "#1E90FF"
    
    svg = f"""
    <svg width="300" height="200" viewBox="0 0 300 200" style="background-color: #f8f9fa; border-radius: 15px; border: 2px solid #ddd;">
        <line x1="150" y1="150" x2="260" y2="150" style="stroke:#333; stroke-width:4; stroke-linecap:round" />
        <line x1="150" y1="150" x2="{x}" y2="{y}" style="stroke:{renk}; stroke-width:5; stroke-linecap:round" />
        <circle cx="150" cy="150" r="6" fill="#333" />
        <path d="M 180 150 A 30 30 0 0 0 {150 + 30 * math.cos(-rad)} {150 + 30 * math.sin(-rad)}" 
              fill="none" stroke="#FFA500" stroke-width="3" />
    </svg>
    """
    return svg

st.title("🎓 Yusuf Agaç: Modern Matematik")

# --- AKILLI ASİSTAN ---
st.info("🤖 **Asistan:** Merhaba Yusuf! Açıları sadece tahmin etmeyeceğiz, türlerini ve matematiksel sırlarını keşfedeceğiz!")

tab1, tab2 = st.tabs(["📐 Açı Laboratuvarı", "🧠 Yeni Nesil Problemler"])

with tab1:
    st.subheader("Açı Türünü Belirle")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(modern_aci_ciz(st.session_state.aci_degeri), unsafe_allow_html=True)
        st.caption("Görseldeki açıyı incele ve karar ver.")
    
    with col2:
        aci_turu = ""
        if st.session_state.aci_degeri < 90: aci_turu = "Dar Açı"
        elif st.session_state.aci_degeri == 90: aci_turu = "Dik Açı"
        elif st.session_state.aci_degeri < 180: aci_turu = "Geniş Açı"
        else: aci_turu = "Doğru Açı"
        
        secenek = st.radio("Bu açı hangi türdür?", ["Dar Açı", "Dik Açı", "Geniş Açı", "Doğru Açı"])
        
        if st.button("Kararımı Verdim"):
            if secenek == aci_turu:
                st.balloons()
                st.success(f"MÜKEMMEL! 🌟 Bu bir **{aci_turu}**. Değeri tam {st.session_state.aci_degeri} derece.")
            else:
                st.error("Hatalı Karar! Asistan Çözümü Gösteriyor:")
                st.markdown(f"""
                <div style="background-color:#fff3e0; padding:15px; border-radius:10px; border-left:5px solid #ff9800;">
                    <strong>📖 Ders Notu:</strong><br>
                    • <b>90°'den küçükse:</b> Dar Açı<br>
                    • <b>Tam 90° ise:</b> Dik Açı (L şekli)<br>
                    • <b>90° - 180° arası ise:</b> Geniş Açı<br>
                    • <b>Tam 180° ise:</b> Doğru Açı (Düz çizgi)
                </div>
                """, unsafe_allow_html=True)

    if st.button("🔄 Başka Bir Açıya Geç"):
        # 5. Sınıf seviyesine uygun "belirgin" açılar seçilir (Çok küçük açılar elendi)
        st.session_state.aci_degeri = random.choice([30, 45, 60, 90, 120, 135, 150, 180])
        st.rerun()

with tab2:
    st.subheader("Yeni Nesil Mantık Sorusu")
    # Dinamik problem üretimi
    nesne = random.choice(["kalem", "çikolata", "sayfa"])
    fiyat = random.randint(5, 15)
    miktar = random.randint(3, 8)
    para = 100
    
    st.write(f"🛒 **Soru:** Yusuf tanesi {fiyat} TL olan {nesne}lerden {miktar} tane alıyor. Kasaya {para} TL verirse kaç TL para üstü almalıdır?")
    
    cevap = st.number_input("Cevabın:", step=1, key="p_cevap")
    dogru = para - (fiyat * miktar)
    
    if st.button("Kontrol Et"):
        if cevap == dogru:
            st.success("Harika bir alışveriş Yusuf! Hesaplaman doğru. ✅")
        else:
            st.error(f"Eyvah, yanlış hesap! Doğru cevap {dogru} TL olmalıydı.")
            st.info(f"💡 **Asistan Çözümü:** {miktar} x {fiyat} = {miktar*fiyat} TL harcadın. {para} - {miktar*fiyat} = {dogru} TL kalır.")
