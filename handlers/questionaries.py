import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.states import Form

from keyboards import inline

from database import requests as rq

router = Router()

#Файл для заполнения формы опроса
#Ввод всех данных через машину состояний (FSM)

@router.callback_query(F.data.startswith("FillForm"))
async def fill_form(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(Form.name)
    await callback_query.message.answer("Введите имя")

@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(Form.surname)
    await message.answer("Введите фамилию")
    
@router.message(Form.surname)
async def form_surname(message: Message, state: FSMContext):
    await state.update_data(surname = message.text)
    await state.set_state(Form.email)
    await message.answer("Введите email")

@router.message(Form.email)
async def form_email(message: Message, state: FSMContext):
    await state.update_data(email = message.text)
    if re.match(r"^\S+@\S+\.\S+$", message.text):
        await state.set_state(Form.phone_number)
        await message.answer("Введите номер телефона в формате '+7XXXXXXXXXX'")
    else:
        await state.set_state(Form.email)
        await message.answer("Введите email корректно!")

@router.message(Form.phone_number)
async def form_phone_number(message: Message, state: FSMContext):
    if message.text[0] == "+" and 12 <= len(message.text) <=14:
        await state.update_data(phone_number = message.text)
        await state.set_state(Form.birth_date)
        await message.answer("Введите вашу дату рождения в формате 01.01.2000")
    else:
        await state.set_state(Form.phone_number)
        await message.answer("Введите номер телефона корректно!")

@router.message(Form.birth_date)
async def form_birth_date(message: Message, state: FSMContext):
    if re.match(r"^\d{2}\.\d{2}\.\d{4}$", message.text):
        await state.update_data(birth_date = message.text)
        
        #Запись всех данных в словарь
        user_data = await state.get_data()
        
        print("Добавление пользователя...")
        print(f"Данные пользователя {user_data}")
        await rq.add_user(
            tg_id = message.from_user.id,
            name = user_data["name"],
            surname = user_data["surname"],
            email = user_data["email"],
            phone_number = user_data["phone_number"],
            birth_date = user_data["birth_date"]
            )
        
        #await message.answer("\n".join(user_data.values()))
    
        await state.clear()
        print("пользователь добавлен")
        await message.answer("Спасибо за заполнение формы! скриншот о прохождении будет отправлен в чат.", reply_markup = inline.end)
        
    else:
        await state.set_state(Form.birth_date)
        await message.answer("Введите дату рождения корректно!")