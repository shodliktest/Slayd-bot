"""Tezis Handler"""
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


class TezisCreation(StatesGroup):
    waiting_conference = State()
    waiting_topic = State()


@router.callback_query(F.data == "create_tezis")
async def start_tezis_creation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TezisCreation.waiting_conference)
    await callback.message.edit_text(
        "📑 <b>KONFERENSIYA TEZISI</b>\n\n"
        "Iltimos, konferensiya nomini kiriting:",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()


@router.message(TezisCreation.waiting_conference)
async def process_conference(message: Message, state: FSMContext):
    conference = message.text.strip()
    await state.update_data(conference=conference)
    await state.set_state(TezisCreation.waiting_topic)
    
    await message.answer(f"✅ Konferensiya: <b>{conference}</b>\n\nEndi mavzuni kiriting:")


@router.message(TezisCreation.waiting_topic)
async def generate_tezis(message: Message, state: FSMContext):
    topic = message.text.strip()
    data = await state.get_data()
    
    await message.answer(
        f"⏳ <b>Tezis tayyorlanmoqda...</b>\n\n"
        f"📚 Konferensiya: {data['conference']}\n"
        f"📝 Mavzu: {topic}\n\n"
        f"<i>Kuting...</i>"
    )
    
    try:
        content = await generator.generate_tezis(
            topic=topic,
            conference=data['conference'],
            pages=3
        )
        
        content_id = f"tezis_{uuid.uuid4().hex[:8]}"
        await tg_db.save_content(content_id, {
            'type': 'tezis',
            'conference': data['conference'],
            'topic': topic,
            'content': content,
            'user_id': message.from_user.id
        })
        
        file = BufferedInputFile(content.encode('utf-8'), filename=f"tezis.txt")
        
        await message.answer_document(
            document=file,
            caption=(
                f"✅ <b>Tezis tayyor!</b>\n\n"
                f"📚 Konferensiya: {data['conference']}\n"
                f"📝 Mavzu: {topic}\n\n"
                f"<i>ID: {content_id}</i>"
            ),
            reply_markup=get_download_keyboard(content_id, "tezis")
        )
        
        await state.clear()
        logger.info(f"Generated tezis: {topic}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer(f"❌ Xatolik: {str(e)}", reply_markup=get_back_keyboard())
        await state.clear()
