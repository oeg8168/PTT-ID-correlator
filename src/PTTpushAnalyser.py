import collections
from src.DBmanage import DBmanage


class PTTpushAnalyser:

    def __init__(self):
        db = DBmanage()

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

    def filterAuthorPusherPair(self, authorPusherPair):
        minDegree = 2
        pairSummary = collections.Counter(authorPusherPair)
        return [x for x in pairSummary if pairSummary[x] >= minDegree]
