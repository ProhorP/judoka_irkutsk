from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def inline_contact_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="VK", url='https://vk.com/sc_judoist')],
        [InlineKeyboardButton(text="Канал", url='https://t.me/JudokaIrkutsk')],
        [InlineKeyboardButton(text="Телефон", callback_data='get_phone')],
        [InlineKeyboardButton(text="2ГИС", url='https://go.2gis.com/ogwBz')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def get_inline_gender_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="👨‍🦱Мужчина", callback_data='Мужчина')],
        [InlineKeyboardButton(text="👩‍🦱Женщина", callback_data='Женщина')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def get_inline_reg_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="✅Да, пройти регистрацию", callback_data='yes')],
        [InlineKeyboardButton(text="❌Без регистрации", callback_data='no')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def get_inline_notify_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="✅Да, отправить пост", callback_data='yes')],
        [InlineKeyboardButton(text="❌Нет", callback_data='no')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def create_qst_inline_kb(questions: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    # Добавляем кнопки вопросов
    for question_id, question_data in questions.items():
        builder.row(
            InlineKeyboardButton(
                text=question_data.get('qst'),
                callback_data=f'qst_{question_id}'
            )
        )
    # Настраиваем размер клавиатуры
    builder.adjust(1)
    return builder.as_markup()
    
def check_data():
    kb_list = [
        [InlineKeyboardButton(text="✅Все верно", callback_data='correct')],
        [InlineKeyboardButton(text="❌Заполнить сначала", callback_data='incorrect')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
