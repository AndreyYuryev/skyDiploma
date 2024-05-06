from telebot.models.models import create_labels
import datetime
import pytest


@pytest.mark.asyncio
async def test_create_labels():
    """ Заполнение меток агрегированных данных """
    from_date = datetime.datetime(2022, 1, 1)
    till_date = datetime.datetime(2022, 1, 8)
    group_type = "day"
    result = ["2022-01-01T00:00:00", "2022-01-02T00:00:00", "2022-01-03T00:00:00", "2022-01-04T00:00:00",
              "2022-01-05T00:00:00", "2022-01-06T00:00:00", "2022-01-07T00:00:00", "2022-01-08T00:00:00", ]
    labels, dataset = await create_labels(from_date, till_date, group_type)
    assert result == labels
    assert len(labels) == len(dataset)
