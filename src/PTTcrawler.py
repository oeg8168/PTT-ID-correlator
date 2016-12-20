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

    def crawlArticlesInBoard(self, boardName):
        boardResultPath = self.databasePath + 'boardResult20161214_' + boardName + '.json'
        print(boardResultPath)

        with open(boardResultPath, encoding='utf8') as f:
            boardResult = json.load(f)
        # print(boardResult)
        # print(len(boardResult['crawlPages']))

        allArticleList = []
        for page in boardResult['crawlPages']:
            allArticleList += page['articleList']
            # print(len(page['articleList']))
            # print()

        # print(allArticleList)
        for articleInfo in allArticleList:
            print(articleInfo['articleID'])
            try:
                article = self.pttParser.parseArticle(boardName, articleInfo['articleID'])
            except Exception as e:
                print('Page Not Found')
            else:
                print('author:', article['authorID'])
                for push in article['pushMessages']:
                    print(push['pushUserID'])
            finally:
                print()

        # crawlResult = {
        #     'timeStamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # }

        # crawlResultFilePath = self.getCrawlResultFilePath(boardName)

    def updateDatabase(self):
        pass
