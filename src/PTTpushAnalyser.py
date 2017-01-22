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

        print('author-pusher pairs filter result')
        print('minDegree set to', minDegree)
        print('before:', len(authorPusherPair))
        print('after :', len(filteredPair))
        print()

        return filteredPair

    def summarizeAuthorPusherPair(self, authorPusherPair,
                                  tagType=['推', '噓', '→']):
        pickedPair = [pair for pair in authorPusherPair if pair[2] in tagType]
        pairSummary = collections.Counter(pickedPair)

        return pairSummary

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
