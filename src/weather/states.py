from aiogram.fsm.state import StatesGroup, State


class Weather(StatesGroup):
    """ The positions of the state machine for transmitting data from the user. """

    city = State()
