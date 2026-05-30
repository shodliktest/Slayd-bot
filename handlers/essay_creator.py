"""Essay Creator Handler"""
import uuid
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import get_word_count_keyboard, get_download_keyboard, get_back_keyboard
from utils.ai_generator import generator
from utils import tg_db

logger = logging.getLogger(__name__)
router = Router()


class EssayCreation(StatesGroup):
    waiting_topic = State()
    waiting_word_count = State()


@router.callback_query(F.data == "create_essay")
async def start_essay_creation(callback: CallbackQuery, state: FSMContext):
    """Start essay creation"""
    
    await state.set_state(EssayCreation.waiting_topic)
    
    text = """
✍️ <b>ESSEY YOZISH</b>

Iltimos, essey uchun mavzuni kiriting:

<i>Misol:
• "Texnologiyaning zamonaviy ta'limga ta'siri"
• "Globalizatsiyaning ijtimoiy oqibatlari"
• "Yoshlarning kasbiy rivojlanishidagi muammolar"</i>

❌ /cancel - Bekor qilish
"""
    
    await callback.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback.answer()


@router.message(EssayCreation.waiting_topic)
async def process_essay_topic(message: Message, state: FSMContext):
    """Process essay topic"""
    
    topic = message.text.strip()
    
    if len(topic) < 10:
        await message.answer("❌ Mavzu juda qisqa. Kamida 10 ta belgi kiriting.")
        return
    
    await state.update_data(topic=topic)
    await state.set_state(EssayCreation.waiting_word_count)
    
    await message.answer(
        f"✅ Mavzu: <b>{topic}</b>\n\n"
        "📝 Necha so'zlik essey kerak?",
        reply_markup=get_word_count_keyboard()
    )


@router.callback_query(F.data.startswith("words:"))
async def process_word_count(callback: CallbackQuery, state: FSMContext):
    """Process word count and generate essay"""
    
    word_count = int(callback.data.split(":")[1])
    data = await state.get_data()
    topic = data['topic']
    
    await callback.message.edit_text(
        f"⏳ <b>Essey yozilmoqda...</b>\n\n"
        f"✍️ Mavzu: {topic}\n"
        f"📝 So'zlar: ~{word_count}\n\n"
        f"<i>Bu bir necha daqiqa vaqt olishi mumkin...</i>"
    )
    await callback.answer()
    
    try:
        essay = await generator.generate_essay(topic=topic, word_count=word_count, language="uz")
        
        content_id = f"essay_{uuid.uuid4().hex[:8]}"
        
        # Save to database
        await tg_db.save_content(content_id, {
            'type': 'essay',
            'topic': topic,
            'word_count': word_count,
            'content': essay,
            'user_id': callback.from_user.id
        })
        
        # Send as document
        file_content = essay.encode('utf-8')
        file = BufferedInputFile(file_content, filename=f"{topic[:30]}.txt")
        
        await callback.message.answer_document(
            document=file,
            caption=(
                f"✅ <b>Essey tayyor!</b>\n\n"
                f"✍️ Mavzu: {topic}\n"
                f"📝 So'zlar: {len(essay.split())} ta\n\n"
                f"<i>ID: {content_id}</i>"
            ),
            reply_markup=get_download_keyboard(content_id, "essay")
        )
        
        await state.clear()
        logger.info(f"Generated essay for user {callback.from_user.id}: {topic}")
        
    except Exception as e:
        logger.error(f"Error generating essay: {e}")
        await callback.message.answer(
            f"❌ Xatolik: {str(e)}\n\nQaytadan urinib ko'ring.",
            reply_markup=get_back_keyboard()
        )
        await state.clear()
