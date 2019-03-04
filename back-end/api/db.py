import dataset
import sqlalchemy.pool


def get_connection() -> dataset.Database:
    return dataset.connect(
        "sqlite:///popular_searches.db",
        engine_kwargs={"connect_args": {"check_same_thread": False}},
    )


def update_popular_searches(name):
    with get_connection() as tx:
        table = tx["popular_searches"]  # type: dataset.Table
        search_count = table.find_one(name=name)
        if search_count:
            row = {"name": search_count["name"], "count": search_count["count"] + 1}
            table.update(row, ["name"])
        else:
            table.insert({"name": name, "count": 1})


def get_popular_searches():
    with get_connection() as tx:
        popular_searches = tx["popular_searches"]  # type: dataset.Table
        return [
            [result["name"]]
            for result in popular_searches.find(_limit=5, order_by=("-count"))
        ]
