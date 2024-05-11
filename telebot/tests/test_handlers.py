from unittest.mock import AsyncMock
import pytest
from telebot.handlers.admin_handlers import answer_if_admins_update, answer_if_admins_update_others
from telebot.handlers.command_handlers import process_start_command, process_help_command
from telebot.handlers.handlers import send_echo
from telebot.lexicon.lexicon import LEXICON_RU
from telebot.config.settings import load_config, Config

@pytest.mark.asyncio
async def test_admins_update():
    message = AsyncMock()
    await answer_if_admins_update(message)
    message.answer.assert_called_with(text=LEXICON_RU['/check'])


@pytest.mark.asyncio
async def test_admins_update_others():
    message = AsyncMock()
    config: Config = load_config()
    await answer_if_admins_update_others(message, config)
    message.answer.assert_called_with(text=LEXICON_RU['adm_upd'])


@pytest.mark.asyncio
async def test_process_start_command():
    message = AsyncMock()
    await process_start_command(message)
    message.answer.assert_called_with(text=LEXICON_RU['/start'])

@pytest.mark.asyncio
async def test_process_help_command():
    message = AsyncMock()
    await process_help_command(message)
    message.answer.assert_called_with(text=LEXICON_RU['/help'])

# @pytest.mark.asyncio
# async def test_json():
#     message = AsyncMock()
#     request: Request = Request(date_from=, date_to=, group_type='month')
#     await process_json_request(message, request, collection)
#     message.answer.assert_called_with(text=LEXICON_RU['/check'])


@pytest.mark.asyncio
async def test_echo():
    message = AsyncMock()
    await send_echo(message)
    message.answer.assert_called_with(text=LEXICON_RU['wrong'])