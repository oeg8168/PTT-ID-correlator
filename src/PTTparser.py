import requests
import json
import re
from bs4 import BeautifulSoup


class PTTparser:

    def __init__(self):
        self.PTTaddress = 'https://www.ptt.cc/bbs/'

    def parseBoard(self, boardName):
        pass

    def parsePage(self, boardName, pageNum):
        pageIndex = '/index' + str(pageNum) + '.html'
        pageURL = self.PTTaddress + boardName + pageIndex
        print(pageURL)
        print('=====')

        response = requests.get(pageURL)
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.find_all('div', class_='title')

        articleList = []
        for t in titles:
            if self.isDeleted(t.text):
                print('deleted page')
            else:
                articleTitle = t.text.strip()
                articleLink = t.find('a').get('href')
                articleID = articleLink.split('/')[3].replace('.html', '')
                article = {
                    'articleTitle': articleTitle,
                    'articleLink': articleLink,
                    'articleID': articleID
                }

                articleList.append(article)

        pageJson = {
            'boardName': boardName,
            'pageNumber': pageNum,
            'articleList': articleList
        }

        print('=====JSON=====')
        jsonText = json.dumps(pageJson, sort_keys=True,
                              indent=4, ensure_ascii=False)
        print(jsonText)

    def isDeleted(self, title):
        if '(本文已被刪除)' in title:
            return True
        elif re.search('(已被.*刪除)', title):
            return True
        else:
            return False

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
