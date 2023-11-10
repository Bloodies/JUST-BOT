from aiogram.fsm.state import State, StatesGroup


class Moon(StatesGroup):
    location = State("Selecting location", "Moon")
    datetime = State("Selecting date", "Moon")
    final = State("Final state", "Moon")
