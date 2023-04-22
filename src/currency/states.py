from aiogram.fsm.state import StatesGroup, State


class Currency(StatesGroup):

    """ The positions of the state machine for transmitting data from the user. """

    TO = State()
    FROM = State()
    AMOUNT = State()