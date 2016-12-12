import json
from os.path import isdir
from os import makedirs
from datetime import datetime
from src.PTTparser import PTTparser


class PTTcrawler:

    def __init__(self):
        self.pttParser = PTTparser()

        self.databasePath = './database/'
        self.createDatabaseFolder()

    def createDatabaseFolder(self):
        if not isdir(self.databasePath):
            print('Database folder not exists!')
            makedirs(self.databasePath)
            print('Created database.')

    def crawlAllBoards(self):
        pass

    def crawlBoard(self, boardName):
        pagesToBeCrawl = 5
        parseBoardResult = self.pttParser.parseBoard(boardName, pagesToBeCrawl)

        crawlResult = {
            'crawlPages': parseBoardResult,
            'crawlPagesCount': len(parseBoardResult),
            'timeStamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        crawlDate = datetime.now().strftime('%Y%m%d')
        dataFileName = 'boardResult' + crawlDate + '_' + boardName + '.json'
        dataFilePath = self.databasePath + dataFileName
        with open(dataFilePath, 'w', encoding='utf-8') as f:
            json.dump(crawlResult, f, sort_keys=True,
                      indent=4, ensure_ascii=False)
            print('Crawl result saved at:', dataFilePath)

    def updateDatabase(self):
        pass
