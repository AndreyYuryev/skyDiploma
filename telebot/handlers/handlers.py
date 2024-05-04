
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from aiogram import Router, F
from filters.filters import IsCorrectRequest, IsJSON
from config.settings import  Request
import logging
from models.models import read_mongo
import asyncio

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
router = Router()


@router.message(F.text, IsJSON(), IsCorrectRequest())
async def process_json_request(message: Message, request: Request, collection):
    """ Хендлер обрабатывающий текстовые сообщения в формате JSON """
    for fut in asyncio.as_completed([read_mongo(request, collection), ]):
        answer = await fut
        await message.answer(text=answer)


@router.message()
async def send_echo(message: Message):
    """ Хендлер обрабатывающий все остальные апдейты """
    try:
        # await message.send_copy(chat_id=message.chat.id)
        await message.answer(text=LEXICON_RU['wrong'])
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])
