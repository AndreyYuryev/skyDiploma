# Описание проекта

## Алгоритм агрегации статистических данных о зарплатах сотрудников компании по временным промежуткам
> Контекст
> 
> На обычном языке пример задачи выглядит следующим образом: “Необходимо посчитать суммы всех выплат с 28.02.2022 по 31.03.2022, единица группировки - день”.

### Описание задач

1. Создать алгоритм агрегации данных
2. Создать телеграм бота, который будет принимать от пользователей текстовые сообщения содержащие JSON с входными данными и отдавать агрегированные данные в ответ.

Алгоритм должен принимать на вход:
1. Дату и время старта агрегации в ISO формате (далее dt_from)
2. Дату и время окончания агрегации в ISO формате (далее dt_upto)
3. Тип агрегации (далее group_type). Типы агрегации могут быть следующие: hour, day, month. То есть группировка всех данных за час, день, неделю, месяц.
```
{"dt_from":"2022-09-01T00:00:00",
"dt_upto":"2022-12-31T23:59:00",
"group_type":"month" }
```
На выходе алгоритм формирует ответ содержащий:**
1. Агрегированный массив данных (далее dataset)
2. Подписи к значениям агрегированного массива данных в ISO формате (далее labels)
```
{"dataset": [5906586, 5515874, 5889803, 6092634], 
"labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", 
"2022-11-01T00:00:00", "2022-12-01T00:00:00"]}
```

### Требования к ландшафту
- Создана база на MongoDB и заполнена необходимыми данными
- Заполнен файл переменных окружения .env на основе .env.sample
- Установлены библиотеки на основе requirements.txt
- Создан телеграм-бот

### Тесты
- Для запуска тестов можно использовать команду `pytest telebot`

## Подготовка проекта к запуску

Проект можно запустить на локальной машине/сервере - для этого необходимо установить БД MongoDB или с помощью Docker, 
для этого необходимо будет установить Docker и поднять контейнеры с MongoDB и приложением на python

### Установка на локальной машине/сервере
1. Склонировать проект ` https://github.com/AndreyYuryev/skyDiploma.git `
2. Установить базу данных MongoDB
3. Создать телеграм бот и получить токен к нему через BotFather
4. Установить необходимые библиотеки из requirements.txt
5. Заполнить файл переменных окружения .env
6. Заполнить базу данных MongoDB данными на основе файла `sample_collection.bson` с помощью команды `mongorestore --u user --p password --authenticationDatabase admin --db database --collection mycollection /data/sample_collection.db` или загрузить данные из файла `sample_collection.json` с помощью MongoDBCompas. Файлы с данными находятся в папке `data` 


### Установка проекта с помощью Docker
Установить можно только контейнер с MondgoDB или запустить весь проект из двух контейнеров для Mongo и приложения.
1. Склонировать проект ` https://github.com/AndreyYuryev/skyDiploma.git `
2. Создать телеграм бот и получить токен к нему через BotFather
3. Заполнить файл переменных окружения .env используя настройки docker-compose.yml
4. Установить необходимые библиотеки из requirements.txt
5. Запустить докер
6. Поднять контейнер с базой данных MongoDB
7. Заполнить базу данных MongoDB данными на основе файла `sample_collection.bson` с помощью команды `mongorestore --u user --p password --authenticationDatabase admin --db newdb --collection mycollection /data/sample_collection.db` или загрузить данные из файла `sample_collection.json` с помощью MongoDBCompas. Файлы с данными находятся в папке `data` 
8. Поднять контейнер с приложением

### Работа с Docker
- Создать образы и контейнеры Docker с помощью команд
  - docker-compose build
  - docker-compose up


### При заполнении базы MongoDB использовалась утилиты `mongosh` и `mongorestore`
### Если использовать локальную MongoDB то загрузку данных выполнять лучше через MongoCompas