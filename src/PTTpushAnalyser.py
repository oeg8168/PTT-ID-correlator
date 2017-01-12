import collections
import networkx as nx
import matplotlib.pyplot as plt

from src.DBmanage import DBmanage


class PTTpushAnalyser:

    def __init__(self):
        self.db = DBmanage()

    def analyseAll(self):
        allAuthorPusherPairs = []
        allArticleResultPath = self.db.getAllLatestArticleResultPath()

        for resultPath in allArticleResultPath:
            crawledArticleResult = self.db.loadCrawledArticleResult(resultPath)
            crawlArticles = crawledArticleResult['crawlArticles']
            allAuthorPusherPairs += self.getAllAuthorPusherPairs(crawlArticles)

        filteredPair = self.filterAuthorPusherPair(allAuthorPusherPairs)

        print('all author-pusher pairs:', len(allAuthorPusherPairs))
        print('filtered author-pusher pairs:', len(filteredPair))

        # NOT DONE YET

    def analyseSingle(self, boardName):
        resultPath = self.db.getLatestArticleResultPath(boardName)

        crawledArticleResult = self.db.loadCrawledArticleResult(resultPath)
        crawlArticles = crawledArticleResult['crawlArticles']
        allAuthorPusherPairs = self.getAllAuthorPusherPairs(crawlArticles)

        filteredPair = self.filterAuthorPusherPair(allAuthorPusherPairs)

        print('all author-pusher pairs:', len(allAuthorPusherPairs))
        print('filtered author-pusher pairs:', len(filteredPair))

        # NOT DONE YET

    def analyse(self):
        pass

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
        return [x for x in pairSummary if pairSummary[x] >= minDegree]

    def summarizeAuthorPusherPair(self, authorPusherPair,
                                  tagType=['推', '噓', '→']):
        pickedPair = [pair for pair in authorPusherPair if pair[2] in tagType]
        pairSummary = collections.Counter(pickedPair)

        return pairSummary

    def createNetworkGraph(self, authorPusherPair):
        graph = nx.DiGraph()
        for pair in authorPusherPair:
            author = pair[0]
            pusher = pair[1]
            graph.add_edge(pusher, author)
            # graph.add_edge(pusher, author, weight=pairSummary[pushPair])

        return graph

    def drawNetworkGraphThenShow(self, graph):
        nx.draw(graph, with_labels=True, font_color='green')
        plt.show()

    def drawNetworkGraphThenSave(self, graph):
        nx.draw(graph, with_labels=True, font_color='green')
        plt.savefig('networkGraph.png')
