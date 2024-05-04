import datetime
import json
import logging
from telebot.config.settings import Request, GROUP_TYPE
from typing import Dict

logger = logging.getLogger(__name__)


async def is_json(value: str) -> bool:
    """ Проверка валидации JSON """
    logger.debug('Проверка JSON внутри функции %s', __name__)
    try:
        # удалить спецсимволы
        # re.sub("^\s+|\n|\r|\s+$", '', value)

        json_dict = json.loads(value)
        return True
    except json.JSONDecodeError:
        logger.error('Некорректный формат JSON', exc_info=True)
        return False


async def is_correct_request(value: str) -> bool | Dict:
    """ Валидация JSON и создание объекта Request """
    logger.debug('Валидация JSON внутри функции %s', __name__)
    try:
        # удалить спецсимволы
        # re.sub("^\s+|\n|\r|\s+$", '', value)

        json_dict = json.loads(value)

        date_from = json_dict.get("dt_from")
        date_upto = json_dict.get("dt_upto")
        group_type = json_dict.get("group_type")

        if (date_from is None or date_upto is None
                or group_type is None
                or group_type not in GROUP_TYPE):
            logger.debug('Некорректный формат запроса')
            return False

        date_fr_list = datetime.datetime.fromisoformat(date_from)
        date_to_list = datetime.datetime.fromisoformat(date_upto)

        datetime_from = datetime.datetime(year=date_fr_list.year,
                                          month=date_fr_list.month,
                                          day=date_fr_list.day,
                                          hour=date_fr_list.hour,
                                          minute=date_fr_list.minute,
                                          second=date_fr_list.second,
                                          tzinfo=date_fr_list.tzinfo)
        datetime_upto = datetime.datetime(year=date_to_list.year,
                                          month=date_to_list.month,
                                          day=date_to_list.day,
                                          hour=date_to_list.hour,
                                          minute=date_to_list.minute,
                                          second=date_to_list.second,
                                          tzinfo=date_to_list.tzinfo)

        if datetime_from > datetime_upto:
            logger.debug('Некорректный диапазон дат')
            return False

        request_object = {"request": Request(dt_from=datetime_from,
                                             dt_upto=datetime_upto,
                                             group_type=group_type)}
        return request_object

    except json.JSONDecodeError:
        logger.error('Некорректный формат JSON', exc_info=True)
        return False
    except ValueError:
        logger.error('Некорректный формат даты', exc_info=True)
        return False
