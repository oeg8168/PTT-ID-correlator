import requests
import json
import re
from bs4 import BeautifulSoup
from os.path import basename


class PTTparser:

    def __init__(self):
        self.PTTaddress = 'https://www.ptt.cc/bbs/'

    def parseBoard(self, boardName):
        pass

    def parsePage(self, boardName, pageNum):
        pageIndex = '/index' + str(pageNum) + '.html'
        pageURL = self.PTTaddress + boardName + pageIndex
        print(pageURL)

        response = requests.get(pageURL)
        html = response.content.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        titles = soup.find_all('div', class_='title')

        articleList = []
        for t in titles:
            if self.isDeleted(t.text):
                pass
            else:
                articleTitle = t.text.strip()
                articleLink = t.find('a').get('href')
                articleID = basename(articleLink).replace('.html', '')
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

        metas = self.getMetasFromArticle(soup)
        allPushs = self.getAllPushsFromArticle(soup)

        articleJSON = {
            'authorID': self.getAuthorIDFromArticle(metas),
            'boardName': boardName,
            'title': self.getTitleFromArticle(metas),
            'postTime': self.getPostTimeFromArticle(metas),
            'pushMessages': self.getPushMessagesFromArticle(allPushs)
        }

        print('=====JSON=====')
        jsonText = json.dumps(articleJSON, sort_keys=True,
                              indent=4, ensure_ascii=False)
        print(jsonText)

    def getMetasFromArticle(self, soup):
        return soup.find_all('span', class_='article-meta-value')
        # return soup.find_all('span', {'class': 'article-meta-value'})

    def getAllPushsFromArticle(self, soup):
        return soup.find_all('div', class_='push')

    def getAuthorIDFromArticle(self, metas):
        return metas[0].text.split(' ')[0]

    def getTitleFromArticle(self, metas):
        return metas[2].text

    def getPostTimeFromArticle(self, metas):
        return metas[3].text

    def getPushMessagesFromArticle(self, allPushs):
        pushMessages = []
        for p in allPushs:
            message = {
                'pushTag': p.find('span', class_='push-tag').text[0],
                'pushUserID': p.find('span', class_='push-userid').text,
                'pushContent': p.find('span', class_='push-content').text[2:]
            }

            pushMessages.append(message)

        return pushMessages
