import asyncio
import logging
# Импортируем драйвер для mongodb
from motor.motor_asyncio import AsyncIOMotorClient
# Импортируем библиотеки телеграма
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
# Импортируем настройки
from telebot.config.settings import Config, load_config, LOGGER_DEBUG
# Импортируем роутеры
from handlers import admin_handlers, handlers, command_handlers
# Импортируем миддлвари
from middlewares.outer import OuterMiddleware
from middlewares.inner import InnerMiddleware
# Импортируем вспомогательные функции для создания нужных объектов
from keyboards.main_menu import set_main_menu

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=(logging.DEBUG if LOGGER_DEBUG else logging.INFO),
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    logger.debug('Загрузка настроек')
    config: Config = load_config()

    # Инициализируем объект хранилища
    logger.debug('Инициализация хранилища')
    storage = MemoryStorage()

    # Инициализируем бот и диспетчер
    logger.debug('Инициализация бота и диспетчера')
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)
    # dp = Dispatcher()

    # Инициализируем другие объекты (пул соединений с БД, кеш и т.п.)
    logger.info('Подключаем базу данных')
    # Connect to the MongoDB instance
    client = AsyncIOMotorClient(config.db.db_host, username=config.db.db_user, password=config.db.db_password)
    collection = client[config.db.database][config.db.collection]
    # # Connect to the MongoDB instance
    # client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")  # , username='root', password='example')
    # # Select the database and collection you want to use
    # db = client["newdb"]
    # collection = db["mycollection"]

    # Помещаем нужные объекты в workflow_data диспетчера
    logger.debug('Подгружаем настройки и коллекцию данных в workflow')
    dp.workflow_data.update({"config": config, "collection": collection})

    # Настраиваем главное меню бота
    logger.debug('Подключаем основное меню')
    await set_main_menu(bot)

    # Регистриуем роутеры
    logger.info('Подключаем роутеры')
    # Регистриуем роутеры в диспетчере
    dp.include_router(command_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(handlers.router)


    # Регистрируем миддлвари
    logger.info('Подключаем миддлвари')
    # Внешние миддлвари
    dp.update.outer_middleware(OuterMiddleware())
    # dp.update.middleware(ThrottlingMiddleware())
    # Внутренние миддлвари
    command_handlers.router.message.middleware(InnerMiddleware())

    # Пропускаем накопившиеся апдейты и запускаем polling
    logger.debug('Запускаем polling')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    """ Запуск асинхронной функции"""
    asyncio.run(main())
