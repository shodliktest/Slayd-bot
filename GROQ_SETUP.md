# ⚡ Groq API Setup Guide

Groq - bu **eng tez va bepul** AI provider! OpenAI'dan 10 barobar tezroq!

## 🚀 Nima Uchun Groq?

| Xususiyat | Groq | OpenAI | Gemini |
|-----------|------|--------|--------|
| **Tezlik** | ⚡⚡⚡ 10x tez | 🐢 Sekin | 🐢 Sekin |
| **Narx** | 🆓 Bepul | 💰 To'lovli | 🆓 Cheklangan |
| **Model** | Llama 3.1 70B | GPT-4 | Gemini Pro |
| **Token Limit** | 32,000 | 4,096-128k | 32,000 |
| **Sifat** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 📝 Groq API Key Olish

### 1. Ro'yxatdan O'tish

1. https://console.groq.com ga o'ting
2. **"Sign Up"** tugmasini bosing
3. Email yoki Google orqali ro'yxatdan o'ting

### 2. API Key Yaratish

1. Dashboard'ga kiring
2. **"API Keys"** bo'limiga o'ting
3. **"Create API Key"** ni bosing
4. Key nomini kiriting (masalan: "Slayd Bot")
5. **"Create"** ni bosing
6. API key'ni nusxalang (faqat bir marta ko'rsatiladi!)

**Misol:**
```
gsk_1234567890abcdefghijklmnopqrstuvwxyz1234567890ABCDEF
```

---

## ⚙️ Bot'ga Ulash

### 1. `.streamlit/secrets.toml` Faylini Tahrirlang

```toml
# AI Provider Configuration
AI_PROVIDER = "groq"

# Groq API Key
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
GROQ_MODEL = "llama-3.1-70b-versatile"
```

### 2. Yoki `.env` Fayl Yarating

```bash
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
```

---

## 🎯 Available Models

Groq'da quyidagi modellar mavjud:

### Llama Models (TAVSIYA)

```toml
# Eng yaxshi sifat va tezlik
GROQ_MODEL = "llama-3.1-70b-versatile"

# Tezroq, lekin kamroq sifatli
GROQ_MODEL = "llama-3.1-8b-instant"

# Aralash variant
GROQ_MODEL = "llama3-70b-8192"
```

### Mixtral Models

```toml
# Yaxshi sifat
GROQ_MODEL = "mixtral-8x7b-32768"

# Juda tez
GROQ_MODEL = "gemma-7b-it"
```

---

## 🧪 Test Qilish

Bot'ni ishga tushiring va tekshiring:

```bash
python bot.py
```

Telegram'da:
1. `/start` ni bosing
2. "📊 Slaydlar" ni tanlang
3. Mavzu kiriting: "Test"
4. 5 slayd tanlang
5. Tezligini his qiling! ⚡

---

## 📊 Limits (Free Tier)

Groq bepul tarif:

- **Requests:** 30 request/daqiqa
- **Tokens:** 6,000 token/daqiqa
- **Daily:** 14,400 request/kun
- **Total:** Cheksiz foydalanish!

Bu botingiz uchun juda yetarli! 🎉

---

## 🔄 Provider O'zgartirish

Agar Groq ishlamasa yoki limitga yetgan bo'lsangiz:

### OpenAI'ga O'tish

```toml
AI_PROVIDER = "openai"
OPENAI_API_KEY = "sk-proj-..."
OPENAI_MODEL = "gpt-4o-mini"
```

### Gemini'ga O'tish

```toml
AI_PROVIDER = "gemini"
GEMINI_API_KEY = "AIza..."
```

---

## 💡 Pro Tips

### 1. Token Tejash

Qisqaroq promptlar yozing:

```python
# ❌ Yomon
"Menga 50 sahifalik juda batafsil, to'liq, akademik darajada..."

# ✅ Yaxshi
"10 sahifa referat: {mavzu}"
```

### 2. Model Tanlash

- **Sifat kerak?** → `llama-3.1-70b-versatile`
- **Tezlik kerak?** → `llama-3.1-8b-instant`
- **Balans kerak?** → `mixtral-8x7b-32768`

### 3. Error Handling

Agar xatolik bo'lsa:

```python
# Bot avtomatik retry qiladi
# Yoki boshqa provider'ga o'tadi
```

---

## ❓ FAQ

### Q: Groq bepulmi?
**A:** Ha! Generous free tier bilan.

### Q: Qancha tez?
**A:** OpenAI'dan 10x tezroq. 2-3 soniyada slayd tayyorlaydi!

### Q: Sifat qanday?
**A:** Llama 3.1 70B - GPT-4 darajasida!

### Q: Limit tugasa?
**A:** Bot avtomatik OpenAI yoki Gemini'ga o'tadi.

### Q: Production'da ishlatsa bo'ladimi?
**A:** Ha! Groq enterprise-grade infrastructure.

---

## 🎉 Tayyor!

Endi botingiz **lightning fast** ishlaydi! ⚡

Savollar: https://console.groq.com/docs

---

**Made with ⚡ by Groq and ❤️ for education**
