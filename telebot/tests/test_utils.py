import pytest
from telebot.filters.filters import IsAdmin
from aiogram.types import Message
from telebot.config.settings import load_config, Request
import datetime
from telebot.utils.checker import is_json, is_correct_request
from unittest.mock import AsyncMock


@pytest.fixture
def mock_message():
    """ Создаем моск для сообщения """
    msg = Message(message_id=123, date=datetime.datetime.today(),
                  chat={"id": 123, "type": "private"},
                  from_user={"id": 870587839, "is_bot": False, "first_name": "Test"})
    return msg


@pytest.mark.asyncio
async def test_filter_is_admin(mock_message):
    """ Тестируем фильтр проверки на админа """
    is_admin = IsAdmin()
    conf = load_config()
    result = await is_admin(mock_message, conf)
    assert result


@pytest.fixture
def correct_json():
    json_str = str('{"dt_from":"2022-09-01T00:00:00", "dt_upto":"2022-12-31T23:59:00", "group_type":"month"}')
    return json_str


@pytest.fixture
def wrong_json():
    json_str = str('{dt_from":"2022-09-01T00:00:00", "dt_upto":"2022-12-31T23:59:00", "group_type":"month"}')
    return json_str


@pytest.fixture
def wrong_date_range_in_json():
    json_str = str('{"dt_from":"2022-09-01T00:00:00", "dt_upto":"2021-12-31T23:59:00", "group_type":"month"}')
    return json_str


@pytest.fixture
def wrong_date_in_json():
    json_str = str('{"dt_from":"2022-09-01T00:00:00", "dt_upto":"2022-14-31T23:59:00", "group_type":"month"}')
    return json_str


@pytest.fixture
def wrong_date_in_json_2():
    json_str = str('{"dt_upto":"2022-14-31T23:59:00", "group_type":"month"}')
    return json_str


@pytest.mark.asyncio
async def test_is_json(correct_json):
    """ Тестируем корректность JSON """
    result = await is_json(correct_json)
    assert result


@pytest.mark.asyncio
async def test_wrong_json(wrong_json):
    """ Тестируем корректность JSON """
    result = await is_json(wrong_json)
    assert not result


@pytest.mark.asyncio
async def test_correct_request(correct_json):
    """ Тестируем корректность запроса """
    correct_request = Request(dt_from=datetime.datetime(2022, 9, 1, 0, 00, 00),
                              dt_upto=datetime.datetime(2022, 12, 31, 23, 59, 00),
                              group_type="month")
    correct_result = dict(request=correct_request)
    result = await is_correct_request(correct_json)
    assert result == correct_result

@pytest.mark.asyncio
async def test_incorrect_json_request(wrong_json):
    """ Тестируем корректность запроса """
    correct_request = Request(dt_from=datetime.datetime(2022, 9, 1, 0, 00, 00),
                              dt_upto=datetime.datetime(2022, 12, 31, 23, 59, 00),
                              group_type="month")
    correct_result = dict(request=correct_request)
    result = await is_correct_request(wrong_json)
    assert not result


@pytest.mark.asyncio
async def test_incorrect_request_range(wrong_date_range_in_json):
    """ Тестируем корректность JSON и некорректность запроса """
    result = await is_json(wrong_date_range_in_json)
    assert result
    result = await is_correct_request(wrong_date_range_in_json)
    assert not result


@pytest.mark.asyncio
async def test_incorrect_request(wrong_date_in_json):
    """ Тестируем корректность JSON и некорректность запроса """
    result = await is_json(wrong_date_in_json)
    assert result
    result = await is_correct_request(wrong_date_in_json)
    assert not result


@pytest.mark.asyncio
async def test_incorrect_request_2(wrong_date_in_json_2):
    """ Тестируем корректность JSON и некорректность запроса """
    result = await is_json(wrong_date_in_json_2)
    assert result
    result = await is_correct_request(wrong_date_in_json_2)
    assert not result


# @pytest.mark.asyncio
# async def test_process_start_command():
#     message = AsyncMock()
#     result = await IsCorre(message)
#     assert result



# @pytest.fixture
# def mock_thing():
#     mock_thing = AsyncMock()
#     mock_thing.the_function_to_mock = AsyncMock(return_value="123")
#     return mock_thing
#
#
# @pytest.mark.asyncio
# async def test_my_test_class(mock_thing):
#     # the patched function can be awaited..
#     result = await mock_thing.the_function_to_mock()
#     assert result == "123"
