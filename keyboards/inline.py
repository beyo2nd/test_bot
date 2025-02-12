from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButtonPollType )

start = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="Начать", callback_data="FillForm")],  # Создаем кнопку с callback_data
            [InlineKeyboardButton(text="О нас", url="https://www.google.ru/")] # Создаем кнопку с url
    ]
)


end = InlineKeyboardMarkup(
    inline_keyboard =[
        [InlineKeyboardButton(text="О нас", url="https://www.google.com/")]
    ]
)