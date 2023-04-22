from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import bot
from .keyboards import get_kb_status_poll, get_kb_other_options
from .states import Poll

router = Router()


@router.message(F.text == "Создать опрос \U0001F5EF")
async def start_create_poll(msg: Message, state: FSMContext):
    await msg.answer("Введите тему опроса", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Poll.question)


@router.message(
    Poll.question,
    F.text.regexp(r".+")
)
async def get_question(msg: Message, state: FSMContext):
    """ Survey topic """

    await state.update_data(question=msg.text, count_option=0, options={})
    await msg.answer("Введите один из вариантов ответа")
    await state.set_state(Poll.options)


@router.message(
    Poll.options,
    F.text.regexp(r".+")
)
async def get_option(msg: Message, state: FSMContext):
    """ Survey response options """

    data = await state.get_data()
    count_option = data.get("count_option") + 1                    # Number of possible answers

    options = data.get("options", {})
    options[f"option_{count_option}"] = msg.text                   # Assigning a new answer option to the previous ones

    await state.update_data(count_option=count_option, options=options)

    if count_option < 2:                                           # Minimum number of possible answers
        await msg.answer("Введите ещё один вариант ответа")
        await state.set_state(Poll.options)
    else:
        if count_option < 10:                                      # Maximum number of possible answers
            await msg.answer("Что дальше?", reply_markup=get_kb_status_poll())
        else:
            await msg.answer("Достигнуто максимальное количество ответов")
        await state.set_state(Poll.status)


@router.message(
    Poll.status,
    F.text.regexp(r".+")
)
async def status_poll(msg: Message, state: FSMContext):
    """ Transition state between adding response options and other settings"""

    if msg.text == 'Отменить всё':                                                     # Resetting the survey settings
        await state.clear()
        await bot.send_message(msg.from_user.id, "Мы переместились в меню!", reply_markup=ReplyKeyboardRemove())
        await msg.delete()
    elif msg.text == "Ввести ещё один вариант ответа":                                 # Adding a new answer option
        await msg.answer("Введите ещё один вариант ответа")
        await state.set_state(Poll.options)
    else:
        await msg.answer("Создать анонимный опрос?", reply_markup=get_kb_other_options())    # Anonymity options
        await state.set_state(Poll.other)


@router.message(
    Poll.other,
    F.text.in_({"Да", "Нет"})
)
async def other_options(msg: Message, state: FSMContext):
    """ Anonymity and multiple response options"""

    data = await state.get_data()
    is_anonymous = data.get("is_anonymous")
    multiple_answer = None

    if is_anonymous is None:                                                     # Status anonymity options
        await state.update_data(is_anonymous=True if msg.text == "Да" else False)
        await msg.answer("Добавить возможность выбора нескольких ответов?", reply_markup=get_kb_other_options())
        await state.set_state(Poll.other)
    elif not is_anonymous is None and multiple_answer is None:                   # Status multiple response options
        multiple_answer = True if msg.text == "Да" and data["count_option"] > 1 else False

    if not is_anonymous is None and not multiple_answer is None:                 # Final statuses of anonymity settings
        question = data["question"]                                              # and multiple responses
        options = [option for option in data["options"].values()]
        await bot.send_poll(
            msg.chat.id, question, options, is_anonymous=is_anonymous, allows_multiple_answers=multiple_answer
        )
        await state.clear()
