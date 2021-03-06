import json
import shutil
import glob

from os import makedirs
from os import listdir
from os.path import isdir
from os.path import basename
from datetime import datetime


class DBmanage:
    def __init__(self):
        self.databasePath = './database/'
        self.subFolderPath = self.databasePath + self.getCrawlDate() + '/'
        self.checkAndCreateDatabaseFolder()

    def getDBPath(self):
        return self.databasePath

    def getSubFolderPath(self):
        return self.subFolderPath

    def checkAndCreateDatabaseFolder(self):
        if not isdir(self.databasePath):
            print('Database folder not exists!')
            makedirs(self.databasePath)
            print('Created database.')

    def checkAndCreateSubFolder(self):
        if not isdir(self.subFolderPath):
            print('Sub-folder not exists!')
            makedirs(self.subFolderPath)
            print('Created subfolder at', self.subFolderPath)

    def removeDatabase(self):
        shutil.rmtree(self.databasePath)
        print('Database removed.')

    def saveResultFile(self, crawlResult, crawlResultFilePath):
        self.checkAndCreateSubFolder()

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
        return self.subFolderPath + crawlResultFileName

    def saveCrawledArticleResult(self, crawlResult):
        boardName = crawlResult['boardName']
        crawlResultFilePath = self.getArticleResultFilePath(boardName)
        self.saveResultFile(crawlResult, crawlResultFilePath)

    def getArticleResultFilePath(self, boardName):
        crawlDate = self.getCrawlDate()
        crawlResultText = 'articleResult' + crawlDate
        crawlResultFileName = crawlResultText + '_' + boardName + '.json'
        return self.subFolderPath + crawlResultFileName

    def loadResultFile(self, path):
        with open(path, encoding='utf8') as f:
            result = json.load(f)
        return result

    def loadCrawledBoardResult(self, boardResultFilePath):
        return self.loadResultFile(boardResultFilePath)

    def loadCrawledArticleResult(self, articleResultFilePath):
        return self.loadResultFile(articleResultFilePath)

    def getLatestVersion(self):
        return listdir(self.databasePath)[-1]

    def getLatestSubFolder(self):
        return self.databasePath + self.getLatestVersion() + '/'

    def getAllLatestBoardResultPath(self):
        latestSubFolder = self.getLatestSubFolder()
        boardResultPattern = latestSubFolder + 'boardResult*.json'
        allBoardResult = glob.glob(boardResultPattern)
        return allBoardResult

    def getAllLatestArticleResultPath(self):
        latestSubFolder = self.getLatestSubFolder()
        articleResultPattern = latestSubFolder + 'articleResult*.json'
        allArticleResult = glob.glob(articleResultPattern)
        return allArticleResult

    def getLatestBoardResultPath(self, boardName):
        latestSubFolder = self.getLatestSubFolder()
        pattern = latestSubFolder + 'boardResult*' + boardName + '.json'
        return glob.glob(pattern)[-1]

    def getLatestArticleResultPath(self, boardName):
        latestSubFolder = self.getLatestSubFolder()
        pattern = latestSubFolder + 'articleResult*' + boardName + '.json'
        return glob.glob(pattern)[-1]

    def getLatestBoardLists(self):
        print('=== Available boards in database ===')
        print('( database version:', self.getLatestVersion(), ')')

        allArticleResultPath = self.getAllLatestArticleResultPath()
        for resultPath in allArticleResultPath:
            fileName = basename(resultPath).replace('.json', '')
            print(fileName.split('_', 1)[1])
