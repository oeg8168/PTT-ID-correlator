import json
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
        pagesToBeCrawl = 2
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
        latestBoardResultPath = self.getLatestBoardResultPath(boardName)

        print('Crawling articles in board...', 'boardname:', boardName)
        print('load boardResult from', latestBoardResultPath)
        with open(latestBoardResultPath, encoding='utf8') as f:
            boardResult = json.load(f)

        allArticleInfoList = self.getAllArticleInfoList(boardResult)

        allArticle = self.getAllArticle(boardName, allArticleInfoList)

        crawlResult = {
            'boardName': boardName,
            'crawlArticles': allArticle,
            'crawlArticlesCount': len(allArticle),
            'timeStamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.db.saveCrawledArticleResult(crawlResult)

    def getLatestBoardResultPath(self, boardName):
        pattern = self.db.getDBPath() + 'boardResult*' + boardName + '.json'
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
