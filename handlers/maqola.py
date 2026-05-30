"""Maqola Handler"""
import uuid
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import get_journal_type_keyboard, get_download_keyboard, get_back_keyboard
from utils.ai_generator import generator
from utils import tg_db

logger = logging.getLogger(__name__)
router = Router()


class MaqolaCreation(StatesGroup):
    waiting_topic = State()
    waiting_journal_type = State()


@router.callback_query(F.data == "create_maqola")
async def start_maqola_creation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MaqolaCreation.waiting_topic)
    await callback.message.edit_text(
        "📰 <b>ILMIY MAQOLA</b>\n\n"
        "Iltimos, maqola mavzusini kiriting:",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()


@router.message(MaqolaCreation.waiting_topic)
async def process_maqola_topic(message: Message, state: FSMContext):
    topic = message.text.strip()
    await state.update_data(topic=topic)
    await state.set_state(MaqolaCreation.waiting_journal_type)
    
    await message.answer(
        f"✅ Mavzu: <b>{topic}</b>\n\n"
        "📚 Jurnal turini tanlang:",
        reply_markup=get_journal_type_keyboard()
    )


@router.callback_query(F.data.startswith("journal:"))
async def generate_maqola(callback: CallbackQuery, state: FSMContext):
    journal_type = callback.data.split(":")[1]
    data = await state.get_data()
    
    await callback.message.edit_text(
        f"⏳ <b>Maqola yozilmoqda...</b>\n\n"
        f"📝 Mavzu: {data['topic']}\n"
        f"📚 Jurnal: {journal_type}\n\n"
        f"<i>Kuting...</i>"
    )
    await callback.answer()
    
    try:
        content = await generator.generate_maqola(
            topic=data['topic'],
            journal_type=journal_type,
            pages=8
        )
        
        content_id = f"maqola_{uuid.uuid4().hex[:8]}"
        await tg_db.save_content(content_id, {
            'type': 'maqola',
            'topic': data['topic'],
            'journal_type': journal_type,
            'content': content,
            'user_id': callback.from_user.id
        })
        
        file = BufferedInputFile(content.encode('utf-8'), filename=f"maqola.txt")
        
        await callback.message.answer_document(
            document=file,
            caption=(
                f"✅ <b>Maqola tayyor!</b>\n\n"
                f"📝 Mavzu: {data['topic']}\n"
                f"📚 Jurnal: {journal_type}\n\n"
                f"<i>ID: {content_id}</i>"
            ),
            reply_markup=get_download_keyboard(content_id, "maqola")
        )
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await callback.message.answer(f"❌ Xatolik: {str(e)}", reply_markup=get_back_keyboard())
        await state.clear()
