# 2b. YAPAY ZEKÂ SORU ÜRETİCİSİ (ÖN TANIMLI KAYNAK)
# OpenAI client'ı sadece API key varsa başlat
try:
    client = OpenAI()  # OPENAI_API_KEY ortam değişkeni gerekli
    OPENAI_AVAILABLE = True
except Exception:
    client = None
    OPENAI_AVAILABLE = False

# Cache için session_state kullan
if 'soru_cache' not in st.session_state:
    st.session_state.soru_cache = {}

def ai_soru_getir(ders, unite, soru_no):
    # Cache kontrolü
    cache_key = f"{ders}_{unite}_{soru_no}"
    if cache_key in st.session_state.soru_cache:
        return st.session_state.soru_cache[cache_key]
    
    if not OPENAI_AVAILABLE:
        result = soru_getir(ders, unite, soru_no)
        st.session_state.soru_cache[cache_key] = result
        return result
    
    prompt = (
        f"5. sınıf seviyesi için {ders} / {unite} konusuna ait "
        f"Türkçe, tek doğru cevaplı bir soru üret. "
        f"JSON olarak dön: " 
        f'{{"soru": "...", "dogru": "...", "yanlislar": ["...","...","..."]}}. '
        f"Yanlışlar anlamca doğruya yakın ama yanlış olsun."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.35,
            max_tokens=300,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )
        content_str = response.choices[0].message.content
        content = json.loads(content_str)
        dogru_cevap = content["dogru"]
        yanlislar = content["yanlislar"]
        secenekler = yanlislar + [dogru_cevap]
        random.shuffle(secenekler)
        result = {
            "soru": content["soru"],
            "A": secenekler[0], "B": secenekler[1], "C": secenekler[2], "D": secenekler[3],
            "dogru_icerik": dogru_cevap
        }
        # Cache'e kaydet
        st.session_state.soru_cache[cache_key] = result
        return result
    except Exception as e:
        st.warning(f"Yapay zekâ sorusu üretilemedi, yerel soruya geçildi. Hata: {e}")
        result = soru_getir(ders, unite, soru_no)
        st.session_state.soru_cache[cache_key] = result
        return result
