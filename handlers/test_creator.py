"""Test Creator Handler"""
import uuid
import json
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import get_question_count_keyboard, get_download_keyboard, get_back_keyboard
from utils.ai_generator import generator
from utils import tg_db

logger = logging.getLogger(__name__)
router = Router()


class TestCreation(StatesGroup):
    waiting_topic = State()
    waiting_count = State()


@router.callback_query(F.data == "create_test")
async def start_test_creation(callback: CallbackQuery, state: FSMContext):
    """Start test creation"""
    
    await state.set_state(TestCreation.waiting_topic)
    
    text = """
❓ <b>TEST TUZISH</b>

Iltimos, test uchun mavzuni kiriting:

<i>Misol:
• "Matematika: Kvadrat tenglamalar"
• "Tarix: O'zbekiston tarixi"
• "Biologiya: Genetika asoslari"</i>

❌ /cancel - Bekor qilish
"""
    
    await callback.message.edit_text(text, reply_markup=get_back_keyboard())
    await callback.answer()


@router.message(TestCreation.waiting_topic)
async def process_test_topic(message: Message, state: FSMContext):
    """Process test topic"""
    
    topic = message.text.strip()
    
    if len(topic) < 5:
        await message.answer("❌ Mavzu juda qisqa.")
        return
    
    await state.update_data(topic=topic)
    await state.set_state(TestCreation.waiting_count)
    
    await message.answer(
        f"✅ Mavzu: <b>{topic}</b>\n\n"
        "📝 Nechta savol kerak?",
        reply_markup=get_question_count_keyboard()
    )


@router.callback_query(F.data.startswith("questions:"))
async def process_question_count(callback: CallbackQuery, state: FSMContext):
    """Generate test questions"""
    
    count = int(callback.data.split(":")[1])
    data = await state.get_data()
    topic = data['topic']
    
    await callback.message.edit_text(
        f"⏳ <b>Test tayyorlanmoqda...</b>\n\n"
        f"❓ Mavzu: {topic}\n"
        f"📝 Savollar: {count} ta\n\n"
        f"<i>Kuting...</i>"
    )
    await callback.answer()
    
    try:
        test_data = await generator.generate_test(topic=topic, count=count, language="uz")
        
        content_id = f"test_{uuid.uuid4().hex[:8]}"
        
        await tg_db.save_content(content_id, {
            'type': 'test',
            'topic': topic,
            'count': count,
            'data': test_data,
            'user_id': callback.from_user.id
        })
        
        # Format test
        test_text = f"TEST: {test_data.get('test_title', topic)}\n\n"
        
        for i, q in enumerate(test_data.get('questions', []), 1):
            test_text += f"{i}. {q['question']}\n"
            for opt in q['options']:
                test_text += f"   {opt}\n"
            test_text += f"   ✅ To'g'ri javob: {q['options'][q['correct_answer']]}\n"
            test_text += f"   💡 Tushuntirish: {q['explanation']}\n\n"
        
        file_content = test_text.encode('utf-8')
        file = BufferedInputFile(file_content, filename=f"test_{topic[:20]}.txt")
        
        await callback.message.answer_document(
            document=file,
            caption=(
                f"✅ <b>Test tayyor!</b>\n\n"
                f"❓ Mavzu: {topic}\n"
                f"📝 Savollar: {len(test_data['questions'])} ta\n\n"
                f"<i>ID: {content_id}</i>"
            ),
            reply_markup=get_download_keyboard(content_id, "test")
        )
        
        await state.clear()
        logger.info(f"Generated test for user {callback.from_user.id}: {topic}")
        
    except Exception as e:
        logger.error(f"Error generating test: {e}")
        await callback.message.answer(
            f"❌ Xatolik: {str(e)}",
            reply_markup=get_back_keyboard()
        )
        await state.clear()
