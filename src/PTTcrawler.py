import glob
from datetime import datetime

from src.PTTparser import PTTparser
from src.DBmanage import DBmanage


class PTTcrawler:

    def __init__(self):
        self.db = DBmanage()
        self.pttParser = PTTparser()

    def crawlHotBoards(self):
        hotBoardList = self.pttParser.parseHotBoard()
        for board in hotBoardList:
            self.crawlBoard(board)
            self.crawlArticlesInBoard(board)

    def crawlBoard(self, boardName):
        pagesToBeCrawl = 10
        print('Crawling board...', 'boardname:', boardName)
        parseBoardResult = self.pttParser.parseBoard(boardName, pagesToBeCrawl)

        crawlResult = {
            'boardName': boardName,
            'crawlPages': parseBoardResult,
            'crawlPagesCount': len(parseBoardResult),
            'timeStamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.db.saveCrawledBoardResult(crawlResult)

    def crawlArticlesInBoard(self, boardName):
        print('Crawling articles in board...', 'boardname:', boardName)

        latestBoardResultPath = self.getLatestBoardResultPath(boardName)
        boardResult = self.db.loadCrawledBoardResult(latestBoardResultPath)
        print('load boardResult from', latestBoardResultPath)

        articleInfoList = self.getArticleInfoList(boardResult)

        allArticle = self.getAllArticle(boardName, articleInfoList)

        crawlResult = {
            'boardName': boardName,
            'crawlArticles': allArticle,
            'crawlArticlesCount': len(allArticle),
            'timeStamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.db.saveCrawledArticleResult(crawlResult)

    def getLatestBoardResultPath(self, boardName):
        fileNamePattern = 'boardResult*' + boardName + '.json'
        pattern = self.db.getSubFolderPath() + fileNamePattern
        return glob.glob(pattern)[-1]

    def getArticleInfoList(self, boardResult):
        articleInfoList = []
        for page in boardResult['crawlPages']:
            articleInfoList += page['articleList']

        return articleInfoList

    def getAllArticle(self, boardName, articleInfoList):
        allArticle = []
        for articleInfo in articleInfoList:
            articleID = articleInfo['articleID']

            print('Board:', boardName, '\t', 'Article ID:', articleID)

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
