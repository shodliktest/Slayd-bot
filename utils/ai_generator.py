"""
AI Content Generator
Supports OpenAI GPT and Google Gemini for content generation
"""
import json
import logging
from typing import Dict, List, Optional
import aiohttp

from config import (
    OPENAI_API_KEY, OPENAI_MODEL, GEMINI_API_KEY, AI_PROVIDER,
    SLIDE_GENERATION_PROMPT_UZ, ESSAY_GENERATION_PROMPT_UZ,
    TEST_GENERATION_PROMPT_UZ, REFERAT_GENERATION_PROMPT_UZ
)

logger = logging.getLogger(__name__)


class AIGenerator:
    """AI content generator with multiple provider support"""
    
    def __init__(self):
        self.provider = AI_PROVIDER
        self.openai_key = OPENAI_API_KEY
        self.gemini_key = GEMINI_API_KEY
        self.model = OPENAI_MODEL
    
    async def generate_slides(
        self,
        topic: str,
        count: int = 10,
        language: str = "uz",
        theme: str = "professional"
    ) -> Dict:
        """Generate presentation slides"""
        
        prompt = SLIDE_GENERATION_PROMPT_UZ.format(topic=topic, count=count)
        
        try:
            if self.provider == "openai":
                response = await self._call_openai(prompt, json_mode=True)
            else:
                response = await self._call_gemini(prompt, json_mode=True)
            
            # Parse JSON response
            slides_data = json.loads(response)
            slides_data['theme'] = theme
            slides_data['language'] = language
            
            logger.info(f"Generated {len(slides_data.get('slides', []))} slides for topic: {topic}")
            return slides_data
            
        except Exception as e:
            logger.error(f"Error generating slides: {e}")
            raise
    
    async def generate_essay(
        self,
        topic: str,
        word_count: int = 1000,
        language: str = "uz"
    ) -> str:
        """Generate essay"""
        
        prompt = ESSAY_GENERATION_PROMPT_UZ.format(
            topic=topic,
            word_count=word_count
        )
        
        try:
            if self.provider == "openai":
                essay = await self._call_openai(prompt)
            else:
                essay = await self._call_gemini(prompt)
            
            logger.info(f"Generated essay for topic: {topic} ({len(essay.split())} words)")
            return essay
            
        except Exception as e:
            logger.error(f"Error generating essay: {e}")
            raise
    
    async def generate_test(
        self,
        topic: str,
        count: int = 20,
        language: str = "uz"
    ) -> Dict:
        """Generate test questions"""
        
        prompt = TEST_GENERATION_PROMPT_UZ.format(topic=topic, count=count)
        
        try:
            if self.provider == "openai":
                response = await self._call_openai(prompt, json_mode=True)
            else:
                response = await self._call_gemini(prompt, json_mode=True)
            
            test_data = json.loads(response)
            
            logger.info(f"Generated {len(test_data.get('questions', []))} questions for topic: {topic}")
            return test_data
            
        except Exception as e:
            logger.error(f"Error generating test: {e}")
            raise
    
    async def generate_referat(
        self,
        topic: str,
        pages: int = 10,
        language: str = "uz"
    ) -> str:
        """Generate referat (research paper)"""
        
        prompt = REFERAT_GENERATION_PROMPT_UZ.format(topic=topic, pages=pages)
        
        try:
            if self.provider == "openai":
                referat = await self._call_openai(prompt)
            else:
                referat = await self._call_gemini(prompt)
            
            logger.info(f"Generated referat for topic: {topic}")
            return referat
            
        except Exception as e:
            logger.error(f"Error generating referat: {e}")
            raise
    
    async def generate_mustaqil_ish(
        self,
        topic: str,
        subject: str,
        pages: int = 15
    ) -> str:
        """Generate independent work (mustaqil ish)"""
        
        prompt = f"""
Sen professional mustaqil ish yozuvchisan. Quyidagi mavzu bo'yicha to'liq mustaqil ish tayyorla.

Fan: {subject}
Mavzu: {topic}
Sahifalar: ~{pages}

Struktura:
1. KIRISH - Mavzu dolzarbligi, maqsad va vazifalar
2. NAZARIY QISM - Nazariy asoslar va adabiyotlar tahlili
3. AMALIY QISM - Amaliy tadqiqotlar va natijalar
4. XULOSA - Asosiy xulosalar va takliflar
5. FOYDALANILGAN ADABIYOTLAR

To'liq akademik formatda yoz.
"""
        
        try:
            if self.provider == "openai":
                content = await self._call_openai(prompt)
            else:
                content = await self._call_gemini(prompt)
            
            logger.info(f"Generated mustaqil ish: {topic}")
            return content
            
        except Exception as e:
            logger.error(f"Error generating mustaqil ish: {e}")
            raise
    
    async def generate_kurs_ishi(
        self,
        topic: str,
        subject: str,
        pages: int = 30
    ) -> str:
        """Generate course work (kurs ishi)"""
        
        prompt = f"""
Sen professional kurs ishi yozuvchisan. Quyidagi mavzu bo'yicha to'liq kurs ishi tayyorla.

Fan: {subject}
Mavzu: {topic}
Sahifalar: ~{pages}

Struktura:
1. MUNDARIJA
2. KIRISH (3-5 sahifa)
   - Mavzu dolzarbligi
   - Maqsad va vazifalar
   - Tadqiqot ob'ekti va predmeti
3. ASOSIY QISM (20-25 sahifa)
   - I BOB: Nazariy asoslar
   - II BOB: Amaliy tahlil
   - III BOB: Takliflar va tavsiyalar
4. XULOSA (2-3 sahifa)
5. FOYDALANILGAN ADABIYOTLAR

Ilmiy uslubda, to'liq akademik formatda yoz.
"""
        
        try:
            if self.provider == "openai":
                content = await self._call_openai(prompt)
            else:
                content = await self._call_gemini(prompt)
            
            logger.info(f"Generated kurs ishi: {topic}")
            return content
            
        except Exception as e:
            logger.error(f"Error generating kurs ishi: {e}")
            raise
    
    async def generate_maqola(
        self,
        topic: str,
        journal_type: str = "ilmiy",
        pages: int = 8
    ) -> str:
        """Generate scientific article (maqola)"""
        
        prompt = f"""
Sen professional ilmiy maqola yozuvchisan. Quyidagi mavzu bo'yicha {journal_type} jurnal uchun maqola tayyorla.

Mavzu: {topic}
Jurnal turi: {journal_type}
Sahifalar: ~{pages}

Struktura:
1. ANNOTATSIYA (150-200 so'z)
2. KALIT SO'ZLAR (5-7 ta)
3. KIRISH - Muammo qo'yilishi
4. ADABIYOTLAR TAHLILI
5. TADQIQOT METODOLOGIYASI
6. NATIJALAR VA MUHOKAMA
7. XULOSA
8. FOYDALANILGAN ADABIYOTLAR (10-15 ta)

Ilmiy uslub, akademik format, manba ko'rsatish bilan yoz.
"""
        
        try:
            if self.provider == "openai":
                content = await self._call_openai(prompt)
            else:
                content = await self._call_gemini(prompt)
            
            logger.info(f"Generated maqola: {topic}")
            return content
            
        except Exception as e:
            logger.error(f"Error generating maqola: {e}")
            raise
    
    async def generate_tezis(
        self,
        topic: str,
        conference: str,
        pages: int = 3
    ) -> str:
        """Generate conference thesis (tezis)"""
        
        prompt = f"""
Sen professional konferensiya tezislari yozuvchisan. Quyidagi mavzu bo'yicha tezis tayyorla.

Konferensiya: {conference}
Mavzu: {topic}
Sahifalar: ~{pages}

Struktura:
1. SARLAVHA
2. MUALLIF(LAR) MA'LUMOTLARI
3. ANNOTATSIYA (100-150 so'z)
4. KALIT SO'ZLAR
5. KIRISH (qisqa)
6. ASOSIY QISM (dolzarbligi, maqsad, natijalar)
7. XULOSA
8. ADABIYOTLAR (3-5 ta)

Ixcham, aniq, ilmiy uslubda yoz.
"""
        
        try:
            if self.provider == "openai":
                content = await self._call_openai(prompt)
            else:
                content = await self._call_gemini(prompt)
            
            logger.info(f"Generated tezis: {topic}")
            return content
            
        except Exception as e:
            logger.error(f"Error generating tezis: {e}")
            raise
    
    async def _call_openai(self, prompt: str, json_mode: bool = False) -> str:
        """Call OpenAI API"""
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Sen professional akademik kontent yaratuvchisan."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OpenAI API error: {response.status} - {error_text}")
                
                data = await response.json()
                return data['choices'][0]['message']['content']
    
    async def _call_gemini(self, prompt: str, json_mode: bool = False) -> str:
        """Call Google Gemini API"""
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4000
            }
        }
        
        if json_mode:
            payload["generationConfig"]["response_mime_type"] = "application/json"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Gemini API error: {response.status} - {error_text}")
                
                data = await response.json()
                return data['candidates'][0]['content']['parts'][0]['text']


# Global generator instance
generator = AIGenerator()
