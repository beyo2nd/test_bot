from aiogram.fsm.state import StatesGroup, State

#Машина состояний

class Form(StatesGroup):
    name = State()
    surname = State()
    email = State()
    phone_number = State()
    birth_date = State ()