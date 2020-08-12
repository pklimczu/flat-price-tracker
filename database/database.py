from tinydb import TinyDB, Query


class DatabaseController:
    """
    Encapsulates operations on TinyDB
    """
    
    def __init__(self, path):
        self.db = TinyDB(path)

        table = self.db.table('test')
        table.insert({'value': True})

        print(self.db.tables())
        print(table.all())


if __name__ == "__main__":
    dc = DatabaseController("db.json")