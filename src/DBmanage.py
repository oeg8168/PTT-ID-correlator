import json
import shutil

from os import makedirs
from os.path import isdir
from datetime import datetime


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

    def saveResultFile(self, crawlResult, crawlResultFilePath):
        with open(crawlResultFilePath, 'w', encoding='utf-8') as f:
            json.dump(crawlResult, f, sort_keys=True,
                      indent=4, ensure_ascii=False)
            print('Crawl result saved at:', crawlResultFilePath)
            print()

    def getCrawlDate(self):
        return datetime.now().strftime('%Y%m%d')

    def saveCrawledBoardResult(self, crawlResult):
        boardName = crawlResult['boardName']
        crawlResultFilePath = self.getBoardResultFilePath(boardName)
        self.saveResultFile(crawlResult, crawlResultFilePath)

    def getBoardResultFilePath(self, boardName):
        crawlDate = self.getCrawlDate()
        crawlResultText = 'boardResult' + crawlDate
        crawlResultFileName = crawlResultText + '_' + boardName + '.json'
        return self.databasePath + crawlResultFileName

    def saveCrawledArticleResult(self, crawlResult):
        boardName = crawlResult['boardName']
        crawlResultFilePath = self.getArticleResultFilePath(boardName)
        self.saveResultFile(crawlResult, crawlResultFilePath)

    def getArticleResultFilePath(self, boardName):
        crawlDate = self.getCrawlDate()
        crawlResultText = 'articleResult' + crawlDate
        crawlResultFileName = crawlResultText + '_' + boardName + '.json'
        return self.databasePath + crawlResultFileName

    def loadResultFile(self, path):
        with open(path, encoding='utf8') as f:
            result = json.load(f)
        return result

    def loadCrawledBoardResult(self, boardResultFilePath):
        return self.loadResultFile(boardResultFilePath)

    def loadCrawledArticleResult(self, articleResultFilePath):
        return self.loadResultFile(articleResultFilePath)
