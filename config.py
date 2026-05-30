"""
Configuration file for AI Slide Generator Bot
"""
import os
from typing import List

# ============================================================================
# TELEGRAM BOT SETTINGS
# ============================================================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_IDS: List[int] = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# Storage channel for database (Telegram kanal ID)
STORAGE_CHANNEL_ID = int(os.getenv("STORAGE_CHANNEL_ID", "-1001234567890"))

# ============================================================================
# AI API SETTINGS
# ============================================================================
# OpenAI API key for content generation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Google Gemini API key (alternative)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Choose AI provider: "openai" or "gemini"
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")

# ============================================================================
# WEB SEARCH SETTINGS
# ============================================================================
# Serper API for web search (https://serper.dev)
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

# Unsplash API for images (https://unsplash.com/developers)
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")

# ============================================================================
# STREAMLIT SETTINGS
# ============================================================================
STREAMLIT_URL = os.getenv("STREAMLIT_URL", "http://localhost:8501")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# ============================================================================
# CONTENT GENERATION LIMITS
# ============================================================================
MAX_SLIDES_PER_REQUEST = 50
MAX_ESSAY_WORDS = 5000
MAX_TEST_QUESTIONS = 100
DEFAULT_SLIDES_COUNT = 10

# ============================================================================
# CACHE SETTINGS
# ============================================================================
RAM_CACHE_MAX_SIZE_MB = 450
CACHE_TTL_HOURS = 48
CLEANUP_INTERVAL_MINUTES = 15

# ============================================================================
# FILE SETTINGS
# ============================================================================
TEMP_FILES_DIR = "/tmp/slayd_bot"
os.makedirs(TEMP_FILES_DIR, exist_ok=True)

# Supported languages
SUPPORTED_LANGUAGES = ["uz", "en", "ru"]
DEFAULT_LANGUAGE = "uz"

# ============================================================================
# PRESENTATION TEMPLATES
# ============================================================================
SLIDE_THEMES = {
    "professional": {
        "bg_color": (255, 255, 255),
        "title_color": (31, 78, 121),
        "text_color": (64, 64, 64),
        "accent_color": (0, 112, 192)
    },
    "modern": {
        "bg_color": (248, 249, 250),
        "title_color": (33, 37, 41),
        "text_color": (73, 80, 87),
        "accent_color": (13, 110, 253)
    },
    "academic": {
        "bg_color": (255, 255, 255),
        "title_color": (139, 0, 0),
        "text_color": (0, 0, 0),
        "accent_color": (139, 69, 19)
    },
    "creative": {
        "bg_color": (255, 250, 240),
        "title_color": (255, 69, 0),
        "text_color": (47, 79, 79),
        "accent_color": (255, 140, 0)
    }
}

DEFAULT_THEME = "professional"

# ============================================================================
# PROMPTS FOR AI
# ============================================================================
SLIDE_GENERATION_PROMPT_UZ = """
Sen professional prezentatsiya mutaxassisisan. Berilgan mavzu bo'yicha akademik darajada slaydlar tayyorla.

Mavzu: {topic}
Slaydlar soni: {count}
Til: O'zbek

Talablar:
1. Har bir slaydda:
   - Qisqa va aniq sarlavha
   - Asosiy fikrlar (3-5 ta bullet points)
   - Ilmiy va akademik yondashuv
   - Misollar va statistika (agar mavzuga mos bo'lsa)

2. Struktura:
   - 1-slayd: Kirish va mavzu taqdimoti
   - O'rta slaydlar: Asosiy ma'lumotlar
   - Oxirgi slayd: Xulosa va tavsiyalar

3. Har bir slaydga mos keladigan rasm keywords ni bering (ingliz tilida)

JSON format:
{{
  "title": "Prezentatsiya sarlavhasi",
  "slides": [
    {{
      "slide_number": 1,
      "title": "Slayd sarlavhasi",
      "content": ["Punkt 1", "Punkt 2", "Punkt 3"],
      "notes": "Qo'shimcha tushuntirishlar",
      "image_keywords": "professional education classroom"
    }}
  ]
}}
"""

ESSAY_GENERATION_PROMPT_UZ = """
Sen professional essay yozuvchisan. Berilgan mavzu bo'yicha akademik darajada essay yoz.

Mavzu: {topic}
So'zlar soni: {word_count}
Til: O'zbek

Struktura:
1. KIRISH (10-15%) - Mavzu taqdimoti, tezis
2. ASOSIY QISM (70-80%) - Dalillar, misollar, tahlil
3. XULOSA (10-15%) - Yakun xulosalar, tavsiyalar

Talablar:
- Akademik uslub
- Ilmiy manbalar
- Mantiqiy oqim
- To'g'ri imlo va tinish belgilari
"""

TEST_GENERATION_PROMPT_UZ = """
Sen professional test tuzuvchisan. Berilgan mavzu bo'yicha test savollari tayyorla.

Mavzu: {topic}
Savollar soni: {count}
Til: O'zbek

Talablar:
1. Har bir savol uchun 4 ta variant
2. Faqat 1 ta to'g'ri javob
3. Qiyinchilik darajasi: oson, o'rta, qiyin (aralash)
4. Mavzuni to'liq qamrab olish

JSON format:
{{
  "test_title": "Test nomi",
  "questions": [
    {{
      "question": "Savol matni",
      "options": ["A) Variant 1", "B) Variant 2", "C) Variant 3", "D) Variant 4"],
      "correct_answer": 0,
      "difficulty": "medium",
      "explanation": "Javob tushuntirilishi"
    }}
  ]
}}
"""

REFERAT_GENERATION_PROMPT_UZ = """
Sen professional referat yozuvchisan. Berilgan mavzu bo'yicha to'liq referat tayyorla.

Mavzu: {topic}
Sahifalar soni: ~{pages}
Til: O'zbek

Struktura:
1. MUNDARIJA
2. KIRISH - Mavzu dolzarbligi, maqsad va vazifalar
3. ASOSIY QISM - Bo'limlar va bo'limchalar
4. XULOSA - Asosiy xulosalar
5. FOYDALANILGAN ADABIYOTLAR

Talablar:
- Akademik format
- Ilmiy uslub
- Manba ko'rsatish
- Tarkibli rejalashtirish
"""
