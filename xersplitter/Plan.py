from os import path
from Table import Table

class Plan:
    def __init__(self, plan_name: str = None):
        self.name = plan_name
        self.tables = []

    def addTable(self, table:Table=None):
        if table:
            self.tables.append(table)

    def load(self, filename):
        extension = ''

        if extension == 'csv':
            self.load_csv(filename)
        elif extension in ('xlsx','xls'):
            self.load_excel(filename)
        else:
            print(f"ERROR: Filetype '{extension}' not supported")
            return

    def load_csv(self, filename):
        return

    def load_excel(self, filename):
        return

    

