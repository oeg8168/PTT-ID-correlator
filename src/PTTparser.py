import requests
import json
from bs4 import BeautifulSoup


class PTTparser:

    def __init__(self):
        self.PTTaddress = 'https://www.ptt.cc/bbs/'

    def parseBoard(self, boardName):
        pass

    def parsePage(self, boardName, pageNum):
        pass

    def parseArticle(self, boardName, articleID):
        articleURL = self.PTTaddress + boardName + '/' + articleID + '.html'
        print(articleURL)

        response = requests.get(articleURL)
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        metas = self.getArticleMeta(soup)
        allPushs = self.getAllPushs(soup)

        articleJSON = {
            'authorID': self.getArticleAuthorID(metas),
            'boardName': boardName,
            'title': self.getArticleTitle(metas),
            'postTime': self.getArticlePostTime(metas),
            'pushMessages': self.getArticlePushMessages(allPushs)
        }

        print('=====JSON=====')
        jsonText = json.dumps(articleJSON, sort_keys=True,
                              indent=4, ensure_ascii=False)
        print(jsonText)

    def getArticleMeta(self, soup):
        return soup.find_all('span', class_='article-meta-value')
        # return soup.find_all('span', {'class': 'article-meta-value'})

    def getAllPushs(self, soup):
        return soup.find_all('div', class_='push')

    def getArticleAuthorID(self, metas):
        return metas[0].text.split(' ')[0]

    def getArticleTitle(self, metas):
        return metas[2].text

    def getArticlePostTime(self, metas):
        return metas[3].text

    def getArticlePushMessages(self, allPushs):
        pushMessages = []
        for p in allPushs:
            message = {
                'pushTag': p.find('span', class_='push-tag').text[0],
                'pushUserID': p.find('span', class_='push-userid').text,
                'pushContent': p.find('span', class_='push-content').text[2:]
            }

            pushMessages.append(message)

        return pushMessages
