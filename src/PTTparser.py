import requests
import re
from time import sleep
from bs4 import BeautifulSoup
from os.path import basename


class PTTparser:

    def __init__(self):
        self.PTTaddress = 'https://www.ptt.cc/bbs/'

    def getSoup(self, URL, encoding='utf-8'):
        response = requests.get(URL, cookies={'over18': '1'})
        if response.status_code != 200:
            raise RuntimeError
        html = response.content.decode(encoding, errors='ignore')
        return BeautifulSoup(html, 'html.parser')

    def parseHotBoard(self):
        hotBoardURL = 'https://www.ptt.cc/hotboard.html'
        soup = self.getSoup(hotBoardURL, 'big5')

        hotBoardTags = soup.find_all('table')

        hotBoardList = []
        for tag in hotBoardTags:
            hotBoardList.append(tag.find_all('td')[1].text)

        # print('=====Hot boards=====')
        # for hb in hotBoardList:
            # print(hb)
        # print('count:', len(hotBoardList))

        return hotBoardList

    def parseBoard(self, boardName, pagesToBeParsed=100):
        boardURL = self.PTTaddress + boardName + '/index.html'
        # print(boardURL)

        soup = self.getSoup(boardURL)

        latestPageNum = self.getLatestPageNum(soup)

        parseResult = []
        parsePageNum = latestPageNum
        for i in range(pagesToBeParsed):
            # print('page: ' + str(parsePageNum))
            parseResult.append(self.parsePage(boardName, parsePageNum))
            parsePageNum -= 1
            print(str(i + 1) + '/' + str(pagesToBeParsed), 'page(s) parsed.')

        sleep(1)
        return parseResult

    def getLatestPageNum(self, soup):
        pagingButtons = soup.find_all('a', class_='btn wide')
        latestPageLink = pagingButtons[1].get('href')
        latestPageNum = re.search('\d+', latestPageLink).group(0)

        return int(latestPageNum)

    def parsePage(self, boardName, pageNum):
        pageIndex = '/index' + str(pageNum) + '.html'
        pageURL = self.PTTaddress + boardName + pageIndex
        # print(pageURL)

        soup = self.getSoup(pageURL)

        allTitleTags = self.getAllTitleTagsFromPage(soup)
        articleList = self.getArticleListFromPage(allTitleTags)

        pageDict = {
            'boardName': boardName,
            'pageNumber': pageNum,
            'articleList': articleList
        }

        # print('=====JSON=====')
        # jsonText = json.dumps(pageDict, sort_keys=True,
        #                       indent=4, ensure_ascii=False)
        # print(jsonText)
        sleep(1)
        return pageDict

    def getAllTitleTagsFromPage(self, soup):
        return soup.find_all('div', class_='title')

    def getArticleListFromPage(self, allTitleTags):
        articleList = []

        for titleTag in allTitleTags:
            if self.isDeleted(titleTag):
                pass
            else:
                articleInfo = self.getArticleInfoFromPage(titleTag)
                articleList.append(articleInfo)

        return articleList

    def isDeleted(self, titleTag):
        if titleTag.find('a') is None:
            return True
        else:
            return False

    def getArticleInfoFromPage(self, titleTag):
        articleTitle = titleTag.text.strip()
        articleLink = titleTag.find('a').get('href')
        articleID = basename(articleLink).replace('.html', '')

        articleInfo = {
            'articleTitle': articleTitle,
            'articleLink': articleLink,
            'articleID': articleID
        }

        return articleInfo

    def parseArticle(self, boardName, articleID):
        articleURL = self.PTTaddress + boardName + '/' + articleID + '.html'
        # print(articleURL)

        soup = self.getSoup(articleURL)

        metas = self.getMetasFromArticle(soup)
        allPushs = self.getAllPushsFromArticle(soup)

        articleDict = {
            'authorID': self.getAuthorIDFromArticle(metas),
            'boardName': boardName,
            'title': self.getTitleFromArticle(metas),
            'postTime': self.getPostTimeFromArticle(metas),
            'pushMessages': self.getPushMessagesFromArticle(allPushs)
        }

        # print('=====JSON=====')
        # jsonText = json.dumps(articleDict, sort_keys=True,
        #                       indent=4, ensure_ascii=False)
        # print(jsonText)
        sleep(1)
        return articleDict

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
