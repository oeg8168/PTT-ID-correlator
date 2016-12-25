import isdir
from os import makedirs


class DBmanage:
    def __init__(self):
        self.databasePath = './database/'

    def createDatabaseFolder(self):
        if not isdir(self.databasePath):
            print('Database folder not exists!')
            makedirs(self.databasePath)
            print('Created database.')

    def updateDatabase(self):
        pass

    def removeDatabase(self):
        pass
