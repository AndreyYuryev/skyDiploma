from dataclasses import dataclass
from environs import Env
from datetime import datetime

# Включить logger для уровня DEBUG
LOGGER_DEBUG = True

GROUP_TYPE = ["hour", "day", "month"]

# Класс данных для базы
@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    collection: str  # Название коллекции
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


# Класс данных для телеграма
@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


# Класс данных для настроек
@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


# Класс данных для запроса
@dataclass
class Request:
    dt_from: datetime
    dt_upto: datetime
    group_type: str


def load_config(path: str | None = None) -> Config:
    ''' Загрузка настроек '''
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            collection=env('COLLECTION'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        )
    )
