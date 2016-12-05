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

        metas = soup.find_all('span', class_='article-meta-value')
        # metas = soup.find_all('span', {'class': 'article-meta-value'})

        author = metas[0].text
        userID = self.getUserID(author)
        boardName = metas[1].text
        title = metas[2].text
        postTime = metas[3].text

        print('Author: ' + author)
        print('User ID: ' + userID)
        print('Board Name: ' + boardName)
        print('Title: ' + title)
        print('Post Time: ' + postTime)

        pushs = soup.find_all('div', class_='push')
        messages = []
        for p in pushs:
            pushTag = p.find('span', class_='push-tag').text
            pushUserID = p.find('span', class_='push-userid').text
            pushContent = p.find('span', class_='push-content').text[2:]

            messages.append({'pushTag': pushTag, 'pushUserID': pushUserID, 'pushContent': pushContent})
            # print(p.text)

        articleJSON = {
            'author': author,
            'userID': userID,
            'boardName': boardName,
            'title': title,
            'postTime': postTime,
            'messages': messages
        }

        print('=====JSON=====')
        print(json.dumps(articleJSON, sort_keys=True, indent=4, ensure_ascii=False))

    def getUserID(self, author):
        return author.split(' ')[0]
