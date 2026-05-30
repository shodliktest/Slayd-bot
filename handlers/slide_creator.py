"""
Slide Creator Handler - PowerPoint presentations
"""
import uuid
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import (
    get_slide_count_keyboard, get_theme_keyboard,
    get_download_keyboard, get_back_keyboard
)
from utils.ai_generator import generator
from utils.pptx_generator import create_presentation_from_data
from utils import tg_db, ram_cache

logger = logging.getLogger(__name__)
router = Router()


class SlideCreation(StatesGroup):
    waiting_topic = State()
    waiting_count = State()
    waiting_theme = State()


@router.callback_query(F.data == "create_slides")
async def start_slide_creation(callback: CallbackQuery, state: FSMContext):
    """Start slide creation process"""
    
    await state.set_state(SlideCreation.waiting_topic)
    
    text = """
📊 <b>SLAYD YARATISH</b>

Iltimos, slaydlar uchun mavzuni kiriting:

<i>Misol:
• "Sun'iy intellekt va uning rivojlanishi"
• "Iqtisodiy globalizatsiya jarayonlari"
• "Ekologik muammolar va ularning yechimlari"</i>

❌ /cancel - Bekor qilish
"""
    
    await callback.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback.answer()


@router.message(SlideCreation.waiting_topic)
async def process_topic(message: Message, state: FSMContext):
    """Process topic input"""
    
    topic = message.text.strip()
    
    if len(topic) < 10:
        await message.answer("❌ Mavzu juda qisqa. Kamida 10 ta belgi kiriting.")
        return
    
    await state.update_data(topic=topic)
    await state.set_state(SlideCreation.waiting_count)
    
    await message.answer(
        f"✅ Mavzu: <b>{topic}</b>\n\n"
        "📝 Nechta slayd kerak?",
        reply_markup=get_slide_count_keyboard()
    )


@router.callback_query(F.data.startswith("slides:"))
async def process_slide_count(callback: CallbackQuery, state: FSMContext):
    """Process slide count selection"""
    
    count = int(callback.data.split(":")[1])
    await state.update_data(count=count)
    await state.set_state(SlideCreation.waiting_theme)
    
    await callback.message.edit_text(
        f"✅ Slaydlar soni: <b>{count}</b>\n\n"
        "🎨 Dizayn turini tanlang:",
        reply_markup=get_theme_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("theme:"))
async def process_theme(callback: CallbackQuery, state: FSMContext):
    """Process theme selection and generate slides"""
    
    theme = callback.data.split(":")[1]
    await state.update_data(theme=theme)
    
    # Get all data
    data = await state.get_data()
    topic = data['topic']
    count = data['count']
    
    await callback.message.edit_text(
        f"⏳ <b>Slaydlar yaratilmoqda...</b>\n\n"
        f"📊 Mavzu: {topic}\n"
        f"📝 Slaydlar: {count} ta\n"
        f"🎨 Dizayn: {theme}\n\n"
        f"<i>Bu bir necha daqiqa vaqt olishi mumkin...</i>"
    )
    await callback.answer()
    
    try:
        # Generate slides content
        slides_data = await generator.generate_slides(
            topic=topic,
            count=count,
            language="uz",
            theme=theme
        )
        
        # Generate PowerPoint file
        content_id = f"slides_{uuid.uuid4().hex[:8]}"
        pptx_path = await create_presentation_from_data(content_id, slides_data)
        
        # Save to database
        await tg_db.save_content(content_id, {
            'type': 'slides',
            'topic': topic,
            'count': count,
            'theme': theme,
            'data': slides_data,
            'user_id': callback.from_user.id
        })
        
        # Send file
        file = FSInputFile(pptx_path)
        await callback.message.answer_document(
            document=file,
            caption=(
                f"✅ <b>Slaydlar tayyor!</b>\n\n"
                f"📊 Mavzu: {topic}\n"
                f"📝 Slaydlar: {len(slides_data['slides'])} ta\n"
                f"🎨 Dizayn: {theme}\n\n"
                f"<i>ID: {content_id}</i>"
            ),
            reply_markup=get_download_keyboard(content_id, "slides")
        )
        
        await state.clear()
        
        logger.info(f"Generated slides for user {callback.from_user.id}: {topic}")
        
    except Exception as e:
        logger.error(f"Error generating slides: {e}")
        await callback.message.answer(
            f"❌ Xatolik yuz berdi: {str(e)}\n\n"
            "Iltimos, qaytadan urinib ko'ring.",
            reply_markup=get_back_keyboard()
        )
        await state.clear()
