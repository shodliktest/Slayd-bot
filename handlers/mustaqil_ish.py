"""Mustaqil Ish Handler"""
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


class MustaqilIshCreation(StatesGroup):
    waiting_subject = State()
    waiting_topic = State()
    waiting_pages = State()


@router.callback_query(F.data == "create_mustaqil")
async def start_mustaqil_creation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(MustaqilIshCreation.waiting_subject)
    await callback.message.edit_text(
        "📄 <b>MUSTAQIL ISH</b>\n\n"
        "Iltimos, fan nomini kiriting:\n\n"
        "<i>Misol: Matematika, Fizika, Tarix</i>",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()


@router.message(MustaqilIshCreation.waiting_subject)
async def process_subject(message: Message, state: FSMContext):
    subject = message.text.strip()
    await state.update_data(subject=subject)
    await state.set_state(MustaqilIshCreation.waiting_topic)
    
    await message.answer(
        f"✅ Fan: <b>{subject}</b>\n\n"
        "Endi mavzuni kiriting:"
    )


@router.message(MustaqilIshCreation.waiting_topic)
async def process_mustaqil_topic(message: Message, state: FSMContext):
    topic = message.text.strip()
    await state.update_data(topic=topic)
    await state.set_state(MustaqilIshCreation.waiting_pages)
    
    await message.answer(
        f"✅ Mavzu: <b>{topic}</b>\n\n"
        "📄 Necha sahifa kerak?",
        reply_markup=get_pages_keyboard()
    )


@router.callback_query(F.data.startswith("pages:"), MustaqilIshCreation.waiting_pages)
async def generate_mustaqil(callback: CallbackQuery, state: FSMContext):
    pages = int(callback.data.split(":")[1])
    data = await state.get_data()
    
    await callback.message.edit_text(
        f"⏳ <b>Mustaqil ish tayyorlanmoqda...</b>\n\n"
        f"📚 Fan: {data['subject']}\n"
        f"📝 Mavzu: {data['topic']}\n"
        f"📄 Sahifalar: ~{pages}\n\n"
        f"<i>Kuting...</i>"
    )
    await callback.answer()
    
    try:
        content = await generator.generate_mustaqil_ish(
            topic=data['topic'],
            subject=data['subject'],
            pages=pages
        )
        
        content_id = f"mustaqil_{uuid.uuid4().hex[:8]}"
        await tg_db.save_content(content_id, {
            'type': 'mustaqil_ish',
            'subject': data['subject'],
            'topic': data['topic'],
            'pages': pages,
            'content': content,
            'user_id': callback.from_user.id
        })
        
        file = BufferedInputFile(content.encode('utf-8'), filename=f"mustaqil_ish.txt")
        
        await callback.message.answer_document(
            document=file,
            caption=(
                f"✅ <b>Mustaqil ish tayyor!</b>\n\n"
                f"📚 Fan: {data['subject']}\n"
                f"📝 Mavzu: {data['topic']}\n"
                f"📄 Sahifalar: ~{pages}\n\n"
                f"<i>ID: {content_id}</i>"
            ),
            reply_markup=get_download_keyboard(content_id, "mustaqil")
        )
        
        await state.clear()
        logger.info(f"Generated mustaqil ish: {data['topic']}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await callback.message.answer(f"❌ Xatolik: {str(e)}", reply_markup=get_back_keyboard())
        await state.clear()
