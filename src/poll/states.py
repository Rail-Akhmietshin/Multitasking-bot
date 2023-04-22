from aiogram.fsm.state import StatesGroup, State


class Poll(StatesGroup):
    """ The positions of the state machine for transmitting data from the user. """

    question = State()
    options = State()                             # Answers
    status = State()                              # Transition state between adding response options and other settings
    other = State()                               # Anonymity and multiple response options

