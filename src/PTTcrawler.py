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

    def crawlHotBoards(self):
        hotBoardList = self.pttParser.parseHotBoard()
        for board in hotBoardList:
            try:
                self.crawlBoard(board)
            except Exception as e:
                print('===Exception Found===')
                print(e)
            else:
                pass
            finally:
                print()

    def crawlBoard(self, boardName):
        pagesToBeCrawl = 5
        parseBoardResult = self.pttParser.parseBoard(boardName, pagesToBeCrawl)

        crawlResult = {
            'crawlPages': parseBoardResult,
            'crawlPagesCount': len(parseBoardResult),
            'timeStamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        crawlResultFilePath = self.getCrawlResultFilePath(boardName)

        self.saveCrawlResultToFile(crawlResult, crawlResultFilePath)

    def getCrawlResultFilePath(self, boardName):
        crawlDate = self.getCrawlDate()
        crawlResultText = 'boardResult' + crawlDate
        crawlResultFileName = crawlResultText + '_' + boardName + '.json'
        return self.databasePath + crawlResultFileName

    def getCrawlDate(self):
        return datetime.now().strftime('%Y%m%d')

    def saveCrawlResultToFile(self, crawlResult, crawlResultFilePath):
        with open(crawlResultFilePath, 'w', encoding='utf-8') as f:
            json.dump(crawlResult, f, sort_keys=True,
                      indent=4, ensure_ascii=False)
            print('Crawl result saved at:', crawlResultFilePath)

    def updateDatabase(self):
        pass
