import json
from os.path import isdir
from os import makedirs
from src.PTTparser import PTTparser


class PTTcrawler:

    def __init__(self):
        self.pttParser = PTTparser()

        self.databasePath = './database/'
        self.createDatabaseFolder()

    def createDatabaseFolder(self):
        if not isdir(self.databasePath):
            print('Database folder not exists!')
            makedirs(self.databasePath)
            print('Created database.')

    def crawl(self):
        parseResult = self.pttParser.parseBoard('Joke', 5)
        # parseResult = self.pttParser.parsePage('Tainan', 3400)
        # jsonText = json.dumps(parseResult, sort_keys=True,
                              # indent=4, ensure_ascii=False)

        dataPath = self.databasePath + 'data.txt'

        with open(dataPath, 'w', encoding='utf-8') as f:
            # f.write(jsonText)
            json.dump(parseResult, f, sort_keys=True,
                      indent=4, ensure_ascii=False)

    def updateDatabase(self):
        pass
