import collections
import networkx as nx
import matplotlib.pyplot as plt

from src.DBmanage import DBmanage


class PTTpushAnalyser:

    def __init__(self):
        self.db = DBmanage()
        self.graph = nx.DiGraph()

    def analyseAll(self):
        allAuthorPusherPairs = []
        allArticleResultPath = self.db.getAllLatestArticleResultPath()

        for resultPath in allArticleResultPath:
            crawledArticleResult = self.db.loadCrawledArticleResult(resultPath)
            crawlArticles = crawledArticleResult['crawlArticles']
            allAuthorPusherPairs += self.getAllAuthorPusherPairs(crawlArticles)

        self.analyse(allAuthorPusherPairs)

    def analyseSingle(self, boardName):
        resultPath = self.db.getLatestArticleResultPath(boardName)

        crawledArticleResult = self.db.loadCrawledArticleResult(resultPath)
        crawlArticles = crawledArticleResult['crawlArticles']
        allAuthorPusherPairs = self.getAllAuthorPusherPairs(crawlArticles)

        self.analyse(allAuthorPusherPairs)

    def analyseByIDinAllBoard(self, queryID):
        allAuthorPusherPairs = []
        allArticleResultPath = self.db.getAllLatestArticleResultPath()

        for resultPath in allArticleResultPath:
            crawledArticleResult = self.db.loadCrawledArticleResult(resultPath)
            crawlArticles = crawledArticleResult['crawlArticles']
            allAuthorPusherPairs += self.getAllAuthorPusherPairs(crawlArticles)

        filteredPair = self.filterAuthorPusherPair(allAuthorPusherPairs)
        filteredPair = self.filterAuthorPusherPairByID(filteredPair, queryID)

        self.createNetworkGraph(filteredPair)

    def analyse(self, allAuthorPusherPairs):
        filteredPair = self.filterAuthorPusherPair(allAuthorPusherPairs)
        self.createNetworkGraph(filteredPair)

    def getAllAuthorPusherPairs(self, crawlArticles):
        allAuthorPusherPairs = []
        for artical in crawlArticles:
            authorID = artical['authorID']
            for push in artical['pushMessages']:
                pushUserID = push['pushUserID']
                pushTag = push['pushTag']
                authorPusherPair = (authorID, pushUserID, pushTag)
                allAuthorPusherPairs.append(authorPusherPair)

        return allAuthorPusherPairs

    def filterAuthorPusherPair(self, authorPusherPair, minDegree=2):
        pairSummary = self.summarizeAuthorPusherPair(authorPusherPair)
        filteredPair = [x for x in pairSummary if pairSummary[x] >= minDegree]

        print('author-pusher pairs filter result (filter by node degree)')
        print('minDegree set to', minDegree)
        self.printFilterInfo(len(authorPusherPair), len(filteredPair))

        return filteredPair

    def filterAuthorPusherPairByID(self, authorPusherPair, queryID):
        filteredPair = [pair for pair in authorPusherPair
                        if queryID in (pair[0], pair[1])]

        print('author-pusher pairs filter result (filter by ID)')
        print('query id:', queryID)
        self.printFilterInfo(len(authorPusherPair), len(filteredPair))

        return filteredPair

    def summarizeAuthorPusherPair(self, authorPusherPair,
                                  tagType=['推', '噓', '→']):
        pickedPair = [pair for pair in authorPusherPair if pair[2] in tagType]
        pairSummary = collections.Counter(pickedPair)

        return pairSummary

    def printFilterInfo(self, before, after):
        print('before:', before)
        print('after :', after)
        print()

    def createNetworkGraph(self, authorPusherPair):
        for pair in authorPusherPair:
            author = pair[0]
            pusher = pair[1]
            self.graph.add_edge(pusher, author)
            # self.graph.add_edge(pusher, author, weight=pairSummary[pushPair])

    def drawNetworkGraphThenShow(self):
        plt.figure(figsize=(8, 8))
        nx.draw(self.graph, with_labels=True, font_color='green')
        plt.show()

    def drawNetworkGraphThenSave(self, path='networkGraph.png'):
        plt.figure(figsize=(8, 8))
        nx.draw(self.graph, with_labels=True, font_color='green')
        plt.savefig(path)
        print('Network graph saved at', path)
