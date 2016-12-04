import requests
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

        metas = soup.find_all('span', class_='article-meta-value')
        # metas = soup.find_all('span', {'class': 'article-meta-value'})

        author = metas[0].text
        boardName = metas[1].text
        title = metas[2].text
        postTime = metas[3].text

        print('Author: ' + author)
        print('Board Name: ' + boardName)
        print('Title: ' + title)
        print('Post Time: ' + postTime)
