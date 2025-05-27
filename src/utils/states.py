from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    PASSWORD_TYPING = State()
