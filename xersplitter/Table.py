class Table:
    def __init__(self, table_name:str=None):
        self.name = table_name
        self.rows = []

    def addData(self, row:list=[]):
        if len(row) > 0:
            self.rows.append(row)

    