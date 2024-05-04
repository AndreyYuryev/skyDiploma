from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from telebot.lexicon.lexicon import LEXICON_RU
from aiogram import Router
import logging


# Инициализируем логгер модуля
logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    """ Хендлер обрабатывающий команду start """
    logger.debug('Вошли в хэндлер, обрабатывающий команду /start')
    await message.answer(text=LEXICON_RU['/start'])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    """ Хендлер обрабатывающий команду help """
    logger.debug('Вошли в хэндлер, обрабатывающий команду /help')
    await message.answer(text=LEXICON_RU['/help'])


@router.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    """ Хендлер обрабатывающий команду stat """
    logger.debug('Вошли в хэндлер, обрабатывающий команду /stat')
    await message.answer(text=LEXICON_RU['/stat'])
