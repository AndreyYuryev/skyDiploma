import datetime
import json
from telebot.config.settings import Request


async def read_mongo(request: Request, collection):
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
    # dt_from = datetime.datetime.fromisoformat(request.dt_from)
    # dt_upto = datetime.datetime.fromisoformat(request.dt_upto)
    #
    # date_from = [dt_from.year, dt_from.month, dt_from.day, dt_from.hour, dt_from.minute, dt_from.second]
    # date_to = [dt_upto.year, dt_upto.month, dt_upto.day, dt_upto.hour, dt_upto.minute, dt_upto.second]
    #
    # # проверка корректности запроса
    #
    #
    #
    #
    # # получение документов коллекции по запросу
    # gte_date = datetime.datetime(year=date_from[0], month=date_from[1], day=date_from[2],
    #                              hour=date_from[3], minute=date_from[4], second=date_from[5])
    # lte_date = datetime.datetime(year=date_to[0], month=date_to[1], day=date_to[2],
    #                              hour=date_to[3], minute=date_to[4], second=date_to[5])



    # создание словаря для записи результатов
    aggregated = dict()
    aggregated["dataset"] = list()
    aggregated["labels"] = list()

    current_date = gte_date
    while current_date <= lte_date:
        # заполнение нулями
        aggregated["dataset"].append(0)
        # заполнение датами
        match group_type:
            case "hour":
                aggregated["labels"].append(datetime.datetime(current_date.year, current_date.month, current_date.day,
                                                              current_date.hour).isoformat())
                current_date = current_date + datetime.timedelta(hours=1)
                current_date = datetime.datetime(current_date.year, current_date.month, current_date.day, current_date.hour)
            case "day":
                aggregated["labels"].append(
                    datetime.datetime(current_date.year, current_date.month, current_date.day).isoformat())
                current_date = current_date + datetime.timedelta(days=1)
                current_date = datetime.datetime(current_date.year, current_date.month, current_date.day)
            case "month":
                aggregated["labels"].append(
                    datetime.datetime(current_date.year, current_date.month, current_date.day).isoformat())
                temp_date = current_date + datetime.timedelta(days=31)
                current_date = datetime.datetime(temp_date.year, temp_date.month, 1)

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


    # формирование json на основе словаря
    json_str = json.dumps(aggregated)
    return json_str

    # # documents = collection.find({"$and": [{"dt": {"$gte": gte_date}},
    # #                                       {"dt": {"$lte": lte_date}}]})
    #
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
    #             current_date = datetime.datetime(current_date.year, current_date.month, current_date.day, current_date.hour)
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
    #
    # # заполнение словаря данными
    # for document in documents:
    #     values = aggregated["dataset"]
    #     labels = aggregated["labels"]
    #
    #     match group_type:
    #         case "hour":
    #             dat = document["dt"]
    #             date_current = datetime.datetime(dat.year, dat.month, dat.day, dat.hour)
    #             index = labels.index(date_current.isoformat())
    #             values[index] += document["value"]
    #         case "day":
    #             dat = document["dt"]
    #             date_current = datetime.datetime(dat.year, dat.month, dat.day)
    #             index = labels.index(date_current.isoformat())
    #             values[index] += document["value"]
    #         case "month":
    #             dat = document["dt"]
    #             date_current = datetime.datetime(dat.year, dat.month, 1)
    #             index = labels.index(date_current.isoformat())
    #             values[index] += document["value"]
    #
    #     # dat = document["dt"]
    #     # values = aggregated["dataset"]
    #     # index = dat.month - 9
    #     # values[index] += document["value"]
    #     # datestr = datetime.datetime(2022, dat.month, 1, 0, 0).isoformat()
    #     #
    #     # aggregated["labels"][index] = datestr
    #     # print(document["dt"])
    #     # print(dat.month)
    #
    # # for key, value in dataset.items():
    # #     print(key, value)
    #
    # # for key, item in aggregated.items():
    # #     print(item)
    #
    # # формирование json на основе словаря
    # json_str = json.dumps(aggregated)
    # return json_str
    # # print(json_str)