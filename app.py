import streamlit as st
import random
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Yusuf AI: Sınav Merkezi", page_icon="📝", layout="centered")

# --- MODERN UI (Görsellerdeki Mobil Uygulama Stili) ---
st.markdown("""
    <style>
    .stApp { background: #f0f2f5; }
    .main-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .question-box { font-size: 20px; font-weight: 600; color: #1e293b; margin-bottom: 20px; padding: 20px; border-left: 5px solid #4f46e5; background: #f8fafc; }
    .stButton>button { border-radius: 12px; height: 3em; font-weight: bold; }
    .status-text { font-size: 14px; color: #64748b; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (KESİNTİSİZ TEST İÇİN) ---
if "page" not in st.session_state: st.session_state.page = "home"
if "score" not in st.session_state: st.session_state.score = 0
if "soru_index" not in st.session_state: st.session_state.soru_index = 0
if "test_sorulari" not in st.session_state: st.session_state.test_sorulari = []
if "yanlis_sayisi" not in st.session_state: st.session_state.yanlis_sayisi = 0
if "toplam_soru_ayarı" not in st.session_state: st.session_state.toplam_soru_ayarı = 20

# --- YENİ NESİL SORU ÜRETİCİ ---
def soru_olustur(ders, zorluk):
    # Bu fonksiyon her çağrıldığında farklı sayılarla yeni nesil soru üretir
    a = random.randint(10, 100)
    b = random.randint(5, 50)
    
    if ders == "Matematik":
        s = f"Yusuf, tanesi {a} TL olan kalemlerden {b} tane alıyor. Kasaya 5000 TL verirse kaç TL para üstü alır?"
        c = str(5000 - (a * b))
        analiz = f"Önce toplam tutarı buluruz ({a}x{b}), sonra 5000'den çıkarırız."
    elif ders == "Fen Bilimleri":
        s = "Dünya, Güneş ve Ay'ın büyüklüklerini birer meyveye benzetecek olursak; Güneş, Dünya ve Ay sırasıyla hangisi olabilir?"
        c = "Karpuz - Nohut - Mercimek"
        analiz = "Güneş en büyük, Ay ise en küçüktür."
    else:
        s = "Aşağıdaki cümlelerin hangisinde 'de' bağlacı yanlış yazılmıştır?"
        c = "Yusuf'da bizimle gelecek."
        analiz = "Bağlaç olan 'da' ayrı yazılır."

    siklar = [c, str(int(c)+10) if c.replace('-','').isdigit() else "Yanlış Şık 1", 
              str(int(c)-5) if c.replace('-','').isdigit() else "Yanlış Şık 2", "Bilmiyorum"]
    random.sample(siklar, len(siklar)) # Karıştır
    return {"s": s, "c": c, "siklar": siklar, "analiz": analiz, "ders": ders}

# --- EKRANLAR ---

# 1. ANA SAYFA
if st.session_state.page == "home":
    st.title("🛡️ Yusuf AI Akademisi")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    st.subheader("Test Ayarlarını Yap")
    secilen_ders = st.selectbox("Ders Seç", ["Matematik", "Fen Bilimleri", "Türkçe"])
    soru_sayisi = st.slider("Soru Sayısı Seç (1-100)", 1, 100, 20)
    st.session_state.toplam_soru_ayarı = soru_sayisi
    
    if st.button("Sınavı Başlat 🚀"):
        # Seçilen sayı kadar soru üret ve hafızaya al
        st.session_state.test_sorulari = [soru_olustur(secilen_ders, "Orta") for _ in range(soru_sayisi)]
        st.session_state.soru_index = 0
        st.session_state.yanlis_sayisi = 0
        st.session_state.page = "quiz"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 2. TEST EKRANI (KESİNTİSİZ)
elif st.session_state.page == "quiz":
    idx = st.session_state.soru_index
    toplam = len(st.session_state.test_sorulari)
    
    if idx < toplam:
        soru = st.session_state.test_sorulari[idx]
        
        st.markdown(f"<p class='status-text'>Soru {idx + 1} / {toplam}</p>", unsafe_allow_html=True)
        st.progress((idx + 1) / toplam)
        
        st.markdown(f"<div class='question-box'>{soru['s']}</div>", unsafe_allow_html=True)
        
        # Şıklar
        cevap = st.radio("Cevabını İşaretle:", soru['siklar'], index=None)
        
        st.divider()
        col1, col2 = st.columns(2)
        
        if col1.button("Sonraki Soru ➡️"):
            if cevap:
                if cevap == soru['c']:
                    st.session_state.score += 10
                    st.toast("Doğru! 🎉")
                else:
                    st.session_state.yanlis_sayisi += 1
                    st.error(f"Yanlış! Doğru cevap: {soru['c']}")
                    st.info(f"📌 Çözüm: {soru['analiz']}")
                    time.sleep(2) # Yanlışı görmesi için kısa bekleme
                
                st.session_state.soru_index += 1
                st.rerun()
            else:
                st.warning("Lütfen bir şık seç!")
        
        if col2.button("Testi Bitir 🏳️"):
            st.session_state.soru_index = toplam
            st.rerun()

    else:
        st.session_state.page = "result"
        st.rerun()

# 3. SONUÇ EKRANI
elif st.session_state.page == "result":
    st.balloons()
    st.title("🏁 Sınav Sonucu")
    st.markdown("<div class='main-card' style='text-align:center;'>", unsafe_allow_html=True)
    
    dogru = st.session_state.toplam_soru_ayarı - st.session_state.yanlis_sayisi
    st.header(f"Skor: {dogru} Doğru / {st.session_state.yanlis_sayisi} Yanlış")
    st.metric("Kazanılan Toplam Puan", st.session_state.score)
    
    if st.button("Yeni Sınava Gir 🔄"):
        st.session_state.page = "home"
        st.session_state.score = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
