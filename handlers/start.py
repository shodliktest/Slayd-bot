"""
Start handler - Welcome message and main menu
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import get_main_menu, get_help_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    
    await state.clear()
    
    welcome_text = """
🎓 <b>Xush Kelibsiz! | Welcome!</b>

Men sizga professional akademik kontent yaratib beraman! 🚀

<b>📚 Quyidagilarni yarata olaman:</b>

✅ <b>Slaydlar (PowerPoint)</b>
   • Professional dizayn
   • Rasmlar bilan
   • Akademik ma'lumotlar

📝 <b>Referatlar</b>
   • To'liq strukturali
   • Ilmiy manbalar bilan

📄 <b>Mustaqil Ish</b>
   • Fan bo'yicha
   • Amaliy qism bilan

📘 <b>Kurs Ishi</b>
   • 30+ sahifa
   • To'liq tadqiqot

📰 <b>Maqola</b>
   • Ilmiy jurnallar uchun
   • Manba ko'rsatish bilan

📑 <b>Tezis</b>
   • Konferensiya uchun
   • Ixcham format

✍️ <b>Essey</b>
   • Har qanday mavzu
   • Akademik uslub

❓ <b>Test</b>
   • Savol-javoblar
   • Tushuntirishlar bilan

---

<b>🎯 Qanday ishlaydi?</b>

1️⃣ Kerakli turni tanlang
2️⃣ Mavzuni kiriting
3️⃣ Qo'shimcha sozlamalar
4️⃣ Bot avtomatik yaratadi! ✨

<b>📲 Boshlash uchun quyidagi tugmalardan birini tanlang:</b>
"""
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_menu()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    
    help_text = """
<b>📖 YORDAM | HELP</b>

<b>🎯 Asosiy buyruqlar:</b>

/start - Botni boshlash
/help - Yordam
/cancel - Jarayonni bekor qilish

<b>📚 Nima yarata olaman?</b>

<b>1. SLAYDLAR (PowerPoint)</b>
• Mavzuni kiriting
• Slaydlar sonini tanlang (5-50)
• Dizayn turini tanlang
• Bot avtomatik ma'lumot topib, rasm qo'shib tayyorlaydi

<b>2. ESSEY</b>
• Mavzu va so'zlar sonini kiriting
• Akademik uslubda yoziladi
• To'liq strukturali (Kirish, Asosiy qism, Xulosa)

<b>3. TEST</b>
• Mavzu va savollar sonini kiriting
• 4 variantli testlar
• To'g'ri javoblar va tushuntirishlar

<b>4. REFERAT</b>
• Mavzu va sahifalar sonini kiriting
• To'liq akademik format
• Manbalar bilan

<b>5. MUSTAQIL ISH</b>
• Fan va mavzuni kiriting
• Nazariy va amaliy qismlar
• Ilmiy yondashuv

<b>6. KURS ISHI</b>
• Fan va mavzuni kiriting
• 30+ sahifa
• To'liq tadqiqot strukturasi

<b>7. MAQOLA</b>
• Mavzu va jurnal turini kiriting
• Ilmiy format
• Manbalar va annotatsiya

<b>8. TEZIS</b>
• Konferensiya va mavzuni kiriting
• Ixcham format (2-3 sahifa)
• Akademik uslub

<b>⚙️ Sozlamalar:</b>

• Til: O'zbek, English, Русский
• Dizayn: Professional, Modern, Academic, Creative
• Hajm: Siz belgilaysiz

<b>❓ Savollar bormi?</b>
@your_support - Qo'llab-quvvatlash
"""
    
    await message.answer(help_text, reply_markup=get_help_keyboard())


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Handle /cancel command"""
    
    await state.clear()
    
    await message.answer(
        "❌ Jarayon bekor qilindi.\n\n"
        "Yangi buyurtma berish uchun /start bosing.",
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Go back to main menu"""
    
    await state.clear()
    
    await callback.message.edit_text(
        "🏠 Asosiy menyu\n\nKerakli bo'limni tanlang:",
        reply_markup=get_main_menu()
    )
    
    await callback.answer()
