"""Kurs Ishi Handler"""
import uuid
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import get_download_keyboard, get_back_keyboard
from utils.ai_generator import generator
from utils import tg_db

logger = logging.getLogger(__name__)
router = Router()


class KursIshiCreation(StatesGroup):
    waiting_subject = State()
    waiting_topic = State()


@router.callback_query(F.data == "create_kurs")
async def start_kurs_creation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(KursIshiCreation.waiting_subject)
    await callback.message.edit_text(
        "📘 <b>KURS ISHI</b>\n\n"
        "Iltimos, fan nomini kiriting:",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()


@router.message(KursIshiCreation.waiting_subject)
async def process_kurs_subject(message: Message, state: FSMContext):
    subject = message.text.strip()
    await state.update_data(subject=subject)
    await state.set_state(KursIshiCreation.waiting_topic)
    
    await message.answer(f"✅ Fan: <b>{subject}</b>\n\nEndi mavzuni kiriting:")


@router.message(KursIshiCreation.waiting_topic)
async def generate_kurs(message: Message, state: FSMContext):
    topic = message.text.strip()
    data = await state.get_data()
    
    await message.answer(
        f"⏳ <b>Kurs ishi tayyorlanmoqda...</b>\n\n"
        f"📚 Fan: {data['subject']}\n"
        f"📝 Mavzu: {topic}\n\n"
        f"<i>Bu 5-10 daqiqa vaqt olishi mumkin...</i>"
    )
    
    try:
        content = await generator.generate_kurs_ishi(
            topic=topic,
            subject=data['subject'],
            pages=30
        )
        
        content_id = f"kurs_{uuid.uuid4().hex[:8]}"
        await tg_db.save_content(content_id, {
            'type': 'kurs_ishi',
            'subject': data['subject'],
            'topic': topic,
            'content': content,
            'user_id': message.from_user.id
        })
        
        file = BufferedInputFile(content.encode('utf-8'), filename=f"kurs_ishi.txt")
        
        await message.answer_document(
            document=file,
            caption=(
                f"✅ <b>Kurs ishi tayyor!</b>\n\n"
                f"📚 Fan: {data['subject']}\n"
                f"📝 Mavzu: {topic}\n"
                f"📄 Sahifalar: ~30\n\n"
                f"<i>ID: {content_id}</i>"
            ),
            reply_markup=get_download_keyboard(content_id, "kurs")
        )
        
        await state.clear()
        logger.info(f"Generated kurs ishi: {topic}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer(f"❌ Xatolik: {str(e)}", reply_markup=get_back_keyboard())
        await state.clear()
