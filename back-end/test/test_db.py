from api import db
from mockito import mock, args
import dataset


class MockTable:
    def __init__(self):
        pass

    def find_one(self, name=None):
        pass

    def find(self, _limit=None, order_by=None):
        pass

    def update(self, row, key):
        pass


class MockDatabase(dict):
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


def test_update_popular_searches(when, expect):
    mock_table = MockTable()
    mock_database = MockDatabase()
    mock_database["popular_searches"] = mock_table

    when(db).get_connection().thenReturn(mock_database)

    expect(mock_table, times=1).find_one(name="anything").thenReturn(
        {"name": "anything", "count": 1}
    )
    expect(mock_table, times=1).update(...)
    db.update_popular_searches("anything")


def test_get_popular_searches(when, expect):
    mock_table = MockTable()
    mock_database = MockDatabase()
    mock_database["popular_searches"] = mock_table

    when(db).get_connection().thenReturn(mock_database)

    expect(mock_table, times=1).find(...).thenReturn(
        [{"name": "anything", "count": 1}]
    )
    popular_searches = db.get_popular_searches()

    assert popular_searches[0][0] == "anything"
