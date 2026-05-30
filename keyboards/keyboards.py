"""
Inline keyboards for bot navigation
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu() -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    
    keyboard = [
        [
            InlineKeyboardButton(text="📊 Slaydlar", callback_data="create_slides"),
            InlineKeyboardButton(text="✍️ Essey", callback_data="create_essay")
        ],
        [
            InlineKeyboardButton(text="❓ Test", callback_data="create_test"),
            InlineKeyboardButton(text="📝 Referat", callback_data="create_referat")
        ],
        [
            InlineKeyboardButton(text="📄 Mustaqil Ish", callback_data="create_mustaqil"),
            InlineKeyboardButton(text="📘 Kurs Ishi", callback_data="create_kurs")
        ],
        [
            InlineKeyboardButton(text="📰 Maqola", callback_data="create_maqola"),
            InlineKeyboardButton(text="📑 Tezis", callback_data="create_tezis")
        ],
        [
            InlineKeyboardButton(text="📖 Yordam", callback_data="show_help"),
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_help_keyboard() -> InlineKeyboardMarkup:
    """Help keyboard"""
    
    keyboard = [
        [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_menu")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Simple back button"""
    
    keyboard = [
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_slide_count_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting number of slides"""
    
    keyboard = [
        [
            InlineKeyboardButton(text="5", callback_data="slides:5"),
            InlineKeyboardButton(text="10", callback_data="slides:10"),
            InlineKeyboardButton(text="15", callback_data="slides:15")
        ],
        [
            InlineKeyboardButton(text="20", callback_data="slides:20"),
            InlineKeyboardButton(text="30", callback_data="slides:30"),
            InlineKeyboardButton(text="50", callback_data="slides:50")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_theme_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting presentation theme"""
    
    keyboard = [
        [
            InlineKeyboardButton(text="💼 Professional", callback_data="theme:professional"),
            InlineKeyboardButton(text="🎨 Modern", callback_data="theme:modern")
        ],
        [
            InlineKeyboardButton(text="🎓 Academic", callback_data="theme:academic"),
            InlineKeyboardButton(text="✨ Creative", callback_data="theme:creative")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_word_count_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting essay word count"""
    
    keyboard = [
        [
            InlineKeyboardButton(text="500", callback_data="words:500"),
            InlineKeyboardButton(text="1000", callback_data="words:1000"),
            InlineKeyboardButton(text="1500", callback_data="words:1500")
        ],
        [
            InlineKeyboardButton(text="2000", callback_data="words:2000"),
            InlineKeyboardButton(text="3000", callback_data="words:3000"),
            InlineKeyboardButton(text="5000", callback_data="words:5000")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_question_count_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting number of test questions"""
    
    keyboard = [
        [
            InlineKeyboardButton(text="10", callback_data="questions:10"),
            InlineKeyboardButton(text="20", callback_data="questions:20"),
            InlineKeyboardButton(text="30", callback_data="questions:30")
        ],
        [
            InlineKeyboardButton(text="50", callback_data="questions:50"),
            InlineKeyboardButton(text="100", callback_data="questions:100")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_pages_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting number of pages"""
    
    keyboard = [
        [
            InlineKeyboardButton(text="5", callback_data="pages:5"),
            InlineKeyboardButton(text="10", callback_data="pages:10"),
            InlineKeyboardButton(text="15", callback_data="pages:15")
        ],
        [
            InlineKeyboardButton(text="20", callback_data="pages:20"),
            InlineKeyboardButton(text="30", callback_data="pages:30"),
            InlineKeyboardButton(text="40", callback_data="pages:40")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting language"""
    
    keyboard = [
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang:uz"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_download_keyboard(content_id: str, content_type: str) -> InlineKeyboardMarkup:
    """Keyboard after content is generated"""
    
    keyboard = [
        [InlineKeyboardButton(text="📥 Yuklash", callback_data=f"download:{content_id}")],
        [InlineKeyboardButton(text="🔄 Qayta yaratish", callback_data=f"regenerate:{content_type}")],
        [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_menu")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_journal_type_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting journal type"""
    
    keyboard = [
        [
            InlineKeyboardButton(text="📚 Ilmiy", callback_data="journal:ilmiy"),
            InlineKeyboardButton(text="📰 Amaliy", callback_data="journal:amaliy")
        ],
        [
            InlineKeyboardButton(text="🎓 O'quv", callback_data="journal:oquv"),
            InlineKeyboardButton(text="🌍 Xalqaro", callback_data="journal:xalqaro")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_menu")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
