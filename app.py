# 2b. YAPAY ZEKÂ SORU ÜRETİCİSİ (ÖN TANIMLI KAYNAK)
# OpenAI client'ı sadece API key varsa başlat
try:
    client = OpenAI()  # OPENAI_API_KEY ortam değişkeni gerekli
    OPENAI_AVAILABLE = True
except Exception:
    client = None
    OPENAI_AVAILABLE = False

@st.cache_data(show_spinner=False)
def ai_soru_getir(ders, unite, soru_no):
    if not OPENAI_AVAILABLE:
        return soru_getir(ders, unite, soru_no)
    
    prompt = (
        f"5. sınıf seviyesi için {ders} / {unite} konusuna ait "
        f"Türkçe, tek doğru cevaplı bir soru üret. "
        f"JSON olarak dön: " 
        f'{{"soru": "...", "dogru": "...", "yanlislar": ["...","...","..."]}}. '
        f"Yanlışlar anlamca doğruya yakın ama yanlış olsun."
    )
    try:
        response = client.chat.completions.create(  # ✅ DÜZELTME: responses.create -> chat.completions.create
            model="gpt-4o-mini",
            temperature=0.35,
            max_tokens=300,  # ✅ DÜZELTME: max_output_tokens -> max_tokens
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]  # ✅ DÜZELTME: input -> messages
        )
        content_str = response.choices[0].message.content  # ✅ DÜZELTME: output_parsed -> choices[0].message.content
        content = json.loads(content_str)  # ✅ JSON parse eklendi
        dogru_cevap = content["dogru"]
        yanlislar = content["yanlislar"]
        secenekler = yanlislar + [dogru_cevap]
        random.shuffle(secenekler)
        return {
            "soru": content["soru"],
            "A": secenekler[0], "B": secenekler[1], "C": secenekler[2], "D": secenekler[3],
            "dogru_icerik": dogru_cevap
        }
    except Exception as e:
        st.warning(f"Yapay zekâ sorusu üretilemedi, yerel soruya geçildi. Hata: {e}")
        return soru_getir(ders, unite, soru_no)
