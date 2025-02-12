from aiogram.types import ( ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType)

#Создание клавиатуры после стартового сообщения

start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Начать"),
            KeyboardButton(text = "О нас" )
        ]
    ],
    resize_keyboard= True,
    one_time_keyboard= True,
    input_field_placeholder= "Выберите действие",
    selective= True
)
