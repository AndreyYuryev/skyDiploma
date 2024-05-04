from aiogram.filters import BaseFilter
from aiogram.types import Message
from config.settings import Config
import logging
from utils.checker import is_json, is_correct_request

logger = logging.getLogger(__name__)


class IsAdmin(BaseFilter):
    """ Класс фильтр возвращающий True если пользователь админ"""

    async def __call__(self, message: Message, config: Config) -> bool:
        logger.debug('Попали внутрь фильтра %s', __class__.__name__)
        return message.from_user.id in config.tg_bot.admin_ids


class IsJSON(BaseFilter):
    """ Класс фильтр возвращающий True если запрос JSON строка """

    async def __call__(self, message: Message) -> bool | dict:
        logger.debug('Попали внутрь фильтра %s', __class__.__name__)
        # parse message to json
        result = await is_json(message.text)
        return result


class IsCorrectRequest(BaseFilter):
    """ Класс фильтр возвращающий True если запрос JSON строка """

    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool | dict:
        """ Метод проверяет полученное сообщение это корректный JSON запрос """
        logger.debug('Попали внутрь фильтра %s', __class__.__name__)
        # parse message to json
        result = await is_correct_request(message.text)
        return result
