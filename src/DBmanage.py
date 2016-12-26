import json
import shutil

from os import makedirs
from os.path import isdir


class DBmanage:
    def __init__(self):
        self.databasePath = './database/'
        self.checkAndCreateDatabaseFolder()

    def getDBPath(self):
        return self.databasePath

    def checkAndCreateDatabaseFolder(self):
        if not isdir(self.databasePath):
            print('Database folder not exists!')
            makedirs(self.databasePath)
            print('Created database.')

    def updateDatabase(self):
        pass

    def removeDatabase(self):
        shutil.rmtree(self.databasePath)
        print('Database removed.')

    def saveCrawlResult(self, crawlResult, crawlResultFilePath):
        with open(crawlResultFilePath, 'w', encoding='utf-8') as f:
            json.dump(crawlResult, f, sort_keys=True,
                      indent=4, ensure_ascii=False)
            print('Crawl result saved at:', crawlResultFilePath)
            print()
