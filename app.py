import streamlit as st
import random
import time
import pandas as pd

# --- SAYFA YAPILANDIRMASI (MOBİL GÖRÜNÜM ODAKLI) ---
st.set_page_config(page_title="Yusuf AI: Akıllı Akademi", page_icon="📱", layout="centered")

# --- PROFESYONEL MOBİL TASARIM (Görsellerdeki Stil) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background: linear-gradient(180deg, #2ecc71 0%, #f1c40f 100%); background-attachment: fixed; }
    
    /* Kategori Kartları (image_ad99bc.jpg'deki gibi) */
    .category-card {
        background: #FF6B6B; color: white; padding: 20px; border-radius: 15px;
        margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-weight: bold; border: 2px solid rgba(255,255,255,0.3);
    }
    
    /* İstatistik Çubukları (image_ad991a.jpg'deki gibi) */
    .stat-row { background: white; border-radius: 10px; padding: 10px; margin-bottom: 8px; border-left: 5px solid #3498db; }
    .progress-bg { background: #eee; border-radius: 20px; height: 10px; width: 100%; margin-top: 5px; }
    .progress-fill { background: #3498db; height: 10px; border-radius: 20px; }
    
    /* Soru Alanı */
    .question-container { background: white; border-radius: 20px; padding: 25px; margin-top: 10px; color: #2c3e50; }
    
    /* Çizim Tahtası Alanı (image_ad99e1.jpg'deki gibi) */
    .scratchpad { border: 2px dashed #bdc3c7; background: #fafafa; height: 100px; border-radius: 10px; text-align: center; color: #95a5a6; padding-top: 35px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (HAFIZA) ---
if "page" not in st.session_state: st.session_state.page = "home"
if "score" not in st.session_state: st.session_state.score = 0
if "history" not in st.session_state: st.session_state.history = []
if "active_test" not in st.session_state: st.session_state.active_test = None

# --- YENİ NESİL SORU BANKASI (Görsellerdeki Örnekler) ---
def soru_getir(kategori):
    if kategori == "Matematik":
        # Abaküs/Ondalık Gösterim Sorusu (image_ad99e1.jpg)
        return {
            "s": "Abaküste binler basamağında 3, ondalık kısımda binde birler basamağında 8 boncuk varsa bu sayı hangisidir?",
            "c": "300,008", "siklar": ["300,008", "30,1518", "301,418", "815,103"],
            "analiz": "Basamak tablosuna yerleştir: Binler(3), Yüzler(0), Onlar(0), Birler(0) , Onda1(0), Yüzde1(0), Binde1(8)."
        }
    elif kategori == "Fen Bilimleri":
        # Güneş Sorusu (image_ad99fb.jpg)
        return {
            "s": "Suna: 'Güneş Dünya'dan büyük müdür?' \nNalan: 'Güneş sıcak gazlardan mı oluşur?' \nSoruların cevapları sırasıyla hangisidir?",
            "c": "Evet - Evet", "siklar": ["Evet - Evet", "Hayır - Evet", "Evet - Hayır", "Hayır - Hayır"],
            "analiz": "Güneş bir yıldızdır, Dünya'dan çok büyüktür ve hidrojen/helyum gazlarından oluşur."
        }
    return {"s": "Örnek Soru", "c": "Cevap", "siklar": ["Cevap", "A", "B", "C"], "analiz": "Açıklama"}

# --- ANA SAYFA (image_ad99a2.jpg ve image_ad99bc.jpg karışımı) ---
if st.session_state.page == "home":
    st.markdown("<h2 style='text-align:center; color:white;'>🏠 Yusuf'un Akademisi</h2>", unsafe_allow_html=True)
    
    # İstatistik Özeti
    st.markdown(f"<div style='text-align:center; color:white; font-size:20px;'>⭐ Toplam Puan: {st.session_state.score}</div>", unsafe_allow_html=True)
    
    # Ders Kategorileri
    dersler = [("🧮 Matematik", "#FF6B6B"), ("📚 Türkçe", "#4D96FF"), ("🧪 Fen Bilimleri", "#6BCB77"), ("🌍 Sosyal Bilgiler", "#FFD93D")]
    
    for ders, renk in dersler:
        if st.button(ders, use_container_width=True):
            st.session_state.active_test = ders.split(" ")[1]
            st.session_state.current_q = soru_getir(st.session_state.active_test)
            st.session_state.page = "test"
            st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)
    if col1.button("📊 Başarı Durumu"): st.session_state.page = "stats"
    if col2.button("⚙️ Ayarlar"): st.toast("Ayarlar yakında!")

# --- TEST SAYFASI (image_ad99dc.jpg ve image_ad99e1.jpg karışımı) ---
elif st.session_state.page == "test":
    q = st.session_state.current_q
    st.markdown(f"<h3 style='text-align:center; color:white;'>{st.session_state.active_test} Testi</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='question-container'>
            <p style='color:#7f8c8d; font-size:12px;'>Soru 1 / 1</p>
            <p style='font-size:18px; font-weight:bold;'>{q['s']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Karalama Tahtası Simülasyonu
    st.markdown("<div class='scratchpad'>✏️ Buraya işlem yapabilirsin (Zihinden veya kağıda)</div>", unsafe_allow_html=True)
    
    # Şıklar (image_ad99fb.jpg tarzı yüzdeli/renkli yapı)
    for sik in q['siklar']:
        if st.button(sik, use_container_width=True):
            if sik == q['c']:
                st.success("🎉 Harika! Doğru Cevap.")
                st.session_state.score += 20
                st.session_state.history.append({"ders": st.session_state.active_test, "durum": "Doğru"})
            else:
                st.error("Hatalı oldu, ama üzülme!")
                st.info(f"💡 Çözüm: {q['analiz']}")
                st.session_state.history.append({"ders": st.session_state.active_test, "durum": "Yanlış"})
            
            time.sleep(2)
            st.session_state.page = "home"
            st.rerun()

    if st.button("⬅️ Testi Bitir"): st.session_state.page = "home"; st.rerun()

# --- İSTATİSTİK SAYFASI (image_ad991a.jpg tarzı) ---
elif st.session_state.page == "stats":
    st.markdown("<h2 style='text-align:center; color:white;'>📊 Ders Başarı Durumu</h2>", unsafe_allow_html=True)
    
    stats_data = [
        ("Matematik", 85), ("Türkçe", 60), ("Fen Bilimleri", 75), ("Sosyal Bilgiler", 90)
    ]
    
    for ders, yuzde in stats_data:
        st.markdown(f"""
            <div class='stat-row'>
                <b>{ders}</b> - %{yuzde} Başarı
                <div class='progress-bg'><div class='progress-fill' style='width:{yuzde}%;'></div></div>
            </div>
        """, unsafe_allow_html=True)
        
    if st.button("🏠 Ana Sayfaya Dön"): st.session_state.page = "home"; st.rerun()
