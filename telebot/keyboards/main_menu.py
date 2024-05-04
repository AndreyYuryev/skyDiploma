from aiogram import Bot
from aiogram.types import BotCommand


# Создаем асинхронную функцию для главного меню
async def set_main_menu(bot: Bot):
    """ Главное меню """
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Добро пожаловать в бот!'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
    ]
    await bot.set_my_commands(main_menu_commands)
