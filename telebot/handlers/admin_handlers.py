
from aiogram.types import Message
from aiogram.filters import Command
from telebot.lexicon.lexicon import LEXICON_RU
from aiogram import Router, F
from telebot.filters.filters import IsAdmin, IsJSON
from telebot.config.settings import Config
import logging

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
router = Router()
# Фильтр для апдейтов для админа
router.message.filter(IsAdmin())


@router.message(Command(commands='check'))
async def answer_if_admins_update(message: Message):
    """ Хендлер обрабатывающий команду check от админа """
    logger.debug('Вошли в хэндлер, обрабатывающий команду /check')
    await message.answer(text=LEXICON_RU['/check'])


@router.message(F.text, ~IsJSON())
async def answer_if_admins_update_others(message: Message, config: Config):
    """ Хендлер обрабатывающий все остальные апдейты от админа """
    logger.debug('Вошли в хэндлер, обрабатывающий сообщения от админа')
    await message.reply(text=LEXICON_RU['adm_upd'])
