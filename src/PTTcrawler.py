import json
import glob
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

        crawlResultFilePath = self.getCrawlBoardResultFilePath(boardName)

        self.saveCrawlResultToFile(crawlResult, crawlResultFilePath)

    def getCrawlBoardResultFilePath(self, boardName):
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
        latestBoardResultPath = self.getLatestBoardResultPath(boardName)
        print(latestBoardResultPath)

        with open(latestBoardResultPath, encoding='utf8') as f:
            boardResult = json.load(f)

        allArticleInfoList = self.getAllArticleInfoList(boardResult)

        allArticle = self.getAllArticle(boardName, allArticleInfoList)

        crawlResult = {
            'crawlArticles': allArticle,
            'crawlArticlesCount': len(allArticle),
            'timeStamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        crawlResultFilePath = self.getCrawlArticleResultFilePath(boardName)

        self.saveCrawlResultToFile(crawlResult, crawlResultFilePath)

    def getLatestBoardResultPath(self, boardName):
        pattern = self.databasePath + 'boardResult*' + boardName + '.json'
        return glob.glob(pattern)[-1]

    def getAllArticleInfoList(self, boardResult):
        allArticleInfoList = []
        for page in boardResult['crawlPages']:
            allArticleInfoList += page['articleList']

        return allArticleInfoList

    def getAllArticle(self, boardName, articleInfoList):
        allArticle = []
        for articleInfo in articleInfoList:
            articleID = articleInfo['articleID']

            print('Board:', boardName)
            print('Article ID:', articleID)

            try:
                article = self.pttParser.parseArticle(boardName, articleID)
            except Exception as e:
                print('Page Not Found')
            else:
                allArticle.append(article)
                print('Parsed successfully.')
            finally:
                print()

        return allArticle

    def getCrawlArticleResultFilePath(self, boardName):
        crawlDate = self.getCrawlDate()
        crawlResultText = 'articleResult' + crawlDate
        crawlResultFileName = crawlResultText + '_' + boardName + '.json'
        return self.databasePath + crawlResultFileName

    def updateDatabase(self):
        pass
