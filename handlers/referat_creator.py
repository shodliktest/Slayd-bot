"""Referat Creator Handler"""
import uuid
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import get_pages_keyboard, get_download_keyboard, get_back_keyboard
from utils.ai_generator import generator
from utils import tg_db

logger = logging.getLogger(__name__)
router = Router()


class ReferatCreation(StatesGroup):
    waiting_topic = State()
    waiting_pages = State()


@router.callback_query(F.data == "create_referat")
async def start_referat_creation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ReferatCreation.waiting_topic)
    await callback.message.edit_text(
        "📝 <b>REFERAT TAYYORLASH</b>\n\n"
        "Iltimos, referat mavzusini kiriting:",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()


@router.message(ReferatCreation.waiting_topic)
async def process_referat_topic(message: Message, state: FSMContext):
    topic = message.text.strip()
    await state.update_data(topic=topic)
    await state.set_state(ReferatCreation.waiting_pages)
    
    await message.answer(
        f"✅ Mavzu: <b>{topic}</b>\n\n📄 Necha sahifa kerak?",
        reply_markup=get_pages_keyboard()
    )


@router.callback_query(F.data.startswith("pages:"))
async def process_pages(callback: CallbackQuery, state: FSMContext):
    pages = int(callback.data.split(":")[1])
    data = await state.get_data()
    topic = data['topic']
    
    await callback.message.edit_text(
        f"⏳ <b>Referat tayyorlanmoqda...</b>\n\n"
        f"📝 Mavzu: {topic}\n"
        f"📄 Sahifalar: ~{pages}\n\n"
        f"<i>Kuting...</i>"
    )
    await callback.answer()
    
    try:
        referat = await generator.generate_referat(topic=topic, pages=pages, language="uz")
        content_id = f"referat_{uuid.uuid4().hex[:8]}"
        
        await tg_db.save_content(content_id, {
            'type': 'referat',
            'topic': topic,
            'pages': pages,
            'content': referat,
            'user_id': callback.from_user.id
        })
        
        file = BufferedInputFile(referat.encode('utf-8'), filename=f"referat_{topic[:20]}.txt")
        
        await callback.message.answer_document(
            document=file,
            caption=f"✅ <b>Referat tayyor!</b>\n\n📝 Mavzu: {topic}\n📄 Sahifalar: ~{pages}\n\n<i>ID: {content_id}</i>",
            reply_markup=get_download_keyboard(content_id, "referat")
        )
        
        await state.clear()
        logger.info(f"Generated referat: {topic}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await callback.message.answer(f"❌ Xatolik: {str(e)}", reply_markup=get_back_keyboard())
        await state.clear()
