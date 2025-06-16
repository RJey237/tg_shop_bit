from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    choosing_language = State()
    entering_name = State()
    entering_phone = State()