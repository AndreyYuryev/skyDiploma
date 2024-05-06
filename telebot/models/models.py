import datetime
import json
from telebot.config.settings import Request
from typing import Dict


async def read_mongo(request: Request, collection) -> str:
    """ Обработка запроса и получение агрегированных данных """
    # # Connect to the MongoDB instance
    # client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")  # , username='root', password='example')
    #
    # # Select the database and collection you want to use
    # db = client["newdb"]
    # collection = db["mycollection"]

    group_type = request.group_type
    gte_date = request.dt_from
    lte_date = request.dt_upto

    # создание словаря для записи результатов
    aggregated = dict()
    aggregated["dataset"] = list()
    aggregated["labels"] = list()

    # async for aggregated["labels"], aggregated["dataset"] in
    aggregated["labels"], aggregated["dataset"] = await create_labels(gte_date, lte_date, group_type)

    # current_date = gte_date
    # while current_date <= lte_date:
    #     # заполнение нулями
    #     aggregated["dataset"].append(0)
    #     # заполнение датами
    #     match group_type:
    #         case "hour":
    #             aggregated["labels"].append(datetime.datetime(current_date.year, current_date.month, current_date.day,
    #                                                           current_date.hour).isoformat())
    #             current_date = current_date + datetime.timedelta(hours=1)
    #             current_date = datetime.datetime(current_date.year, current_date.month, current_date.day,
    #                                              current_date.hour)
    #         case "day":
    #             aggregated["labels"].append(
    #                 datetime.datetime(current_date.year, current_date.month, current_date.day).isoformat())
    #             current_date = current_date + datetime.timedelta(days=1)
    #             current_date = datetime.datetime(current_date.year, current_date.month, current_date.day)
    #         case "month":
    #             aggregated["labels"].append(
    #                 datetime.datetime(current_date.year, current_date.month, current_date.day).isoformat())
    #             temp_date = current_date + datetime.timedelta(days=31)
    #             current_date = datetime.datetime(temp_date.year, temp_date.month, 1)

    # cursor = collection.find({"$and": [{"dt": {"$gte": gte_date}}, {"dt": {"$lte": lte_date}}]})

    # for documents in await cursor.to_list():
    # while await cursor.fetch_next:
    #     documents = cursor.next_object()
    async for documents in collection.find({"$and": [{"dt": {"$gte": gte_date}}, {"dt": {"$lte": lte_date}}]}):
        # pprint.pprint(documents)
        # заполнение словаря данными
        values = aggregated["dataset"]
        labels = aggregated["labels"]

        match group_type:
            case "hour":
                dat = documents["dt"]
                date_current = datetime.datetime(dat.year, dat.month, dat.day, dat.hour)
                index = labels.index(date_current.isoformat())
                values[index] += documents["value"]
            case "day":
                dat = documents["dt"]
                date_current = datetime.datetime(dat.year, dat.month, dat.day)
                index = labels.index(date_current.isoformat())
                values[index] += documents["value"]
            case "month":
                dat = documents["dt"]
                date_current = datetime.datetime(dat.year, dat.month, 1)
                index = labels.index(date_current.isoformat())
                values[index] += documents["value"]

    # # формирование json на основе словаря
    json_str = json.dumps(aggregated)
    # print(len(aggregated['dataset']), json_str)
    return json_str


async def create_labels(from_date: datetime, till_date: datetime, group_type) -> list:
    current_date = from_date
    labels = list()
    dataset = list()
    while current_date <= till_date:
        # заполнение нулями
        dataset.append(0)
        # заполнение датами
        match group_type:
            case "hour":
                labels.append(datetime.datetime(current_date.year, current_date.month, current_date.day,
                                                current_date.hour).isoformat())
                current_date = current_date + datetime.timedelta(hours=1)
                current_date = datetime.datetime(current_date.year, current_date.month, current_date.day,
                                                 current_date.hour)
            case "day":
                labels.append(
                    datetime.datetime(current_date.year, current_date.month, current_date.day).isoformat())
                current_date = current_date + datetime.timedelta(days=1)
                current_date = datetime.datetime(current_date.year, current_date.month, current_date.day)
            case "month":
                labels.append(
                    datetime.datetime(current_date.year, current_date.month, current_date.day).isoformat())
                temp_date = current_date + datetime.timedelta(days=31)
                current_date = datetime.datetime(temp_date.year, temp_date.month, 1)
    return labels, dataset
