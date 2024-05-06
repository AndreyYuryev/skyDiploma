from aiogram.types import Message
from telebot.lexicon.lexicon import LEXICON_RU
from aiogram import Router, F
from telebot.filters.filters import IsCorrectRequest, IsJSON
from telebot.config.settings import Request
import logging
from telebot.models.models import read_mongo
import asyncio

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
router = Router()


@router.message(F.text, IsJSON(), IsCorrectRequest())
async def process_json_request(message: Message, request: Request, collection):
    """ Хендлер обрабатывающий текстовые сообщения в формате JSON """
    MAX_SYMBOLS = 4095
    for fut in asyncio.as_completed([read_mongo(request, collection), ]):
        answer = await fut
        if len(answer) > MAX_SYMBOLS:
            for item in range(len(answer) // MAX_SYMBOLS + 1):
                splitted = answer[item * MAX_SYMBOLS:item * MAX_SYMBOLS + MAX_SYMBOLS]
                await message.answer(text=splitted)
        else:
            await message.answer(text=answer)


@router.message()
async def send_echo(message: Message):
    """ Хендлер обрабатывающий все остальные апдейты """
    try:
        # await message.send_copy(chat_id=message.chat.id)
        await message.answer(text=LEXICON_RU['wrong'])
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])
