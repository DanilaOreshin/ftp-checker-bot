from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    WAITING = State()
