import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, Update

logger = logging.getLogger(__name__)


class InnerMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        logger.debug(
            'Вошли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__
        )

        update: Update = data.get("event_update")
        message: Message = update.message
        entities: list = message.entities
        if entities is None:
            return logger.debug('Это не команда. Выходим из миддлвари  %s', __class__.__name__)

        result = await handler(event, data)
        logger.debug('Выходим из миддлвари  %s', __class__.__name__)
        return result
