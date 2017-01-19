import argparse

from src.PTTcrawler import PTTcrawler
from src.PTTpushAnalyser import PTTpushAnalyser
from src.DBmanage import DBmanage


def main():
    args = parseArguments()

    pushAnalyser = PTTpushAnalyser()

    if args.update:
        print('=== update ===')
        crawler = PTTcrawler()
        crawler.crawlHotBoards()

    elif args.view_board_list:
        db = DBmanage()
        db.getLatestBoardLists()

    elif args.run_save_all:
        print('=== run save all ===')
        pushAnalyser.analyseAll()
        pushAnalyser.drawNetworkGraphThenSave()

    elif args.run_show_all:
        print('=== run show all ===')
        pushAnalyser.analyseAll()
        pushAnalyser.drawNetworkGraphThenShow()

    elif args.run_save:
        print('=== run save', args.run_save, '===')
        pushAnalyser.analyseSingle(args.run_save)
        pushAnalyser.drawNetworkGraphThenSave()

    elif args.run_show:
        print('=== run show', args.run_show, '===')
        pushAnalyser.analyseSingle(args.run_show)
        pushAnalyser.drawNetworkGraphThenShow()


def parseArguments():
    cmdArgsParser = argparse.ArgumentParser()
    cmdGroup = cmdArgsParser.add_mutually_exclusive_group(required=True)

    cmdGroup.add_argument('--update', action='store_true',
                          help='Update database')

    cmdGroup.add_argument('--view_board_list', action='store_true',
                          help='View available boards in latest database')

    cmdGroup.add_argument('--run_save_all', action='store_true',
                          help='Run and save as imagefile (all board)')

    cmdGroup.add_argument('--run_show_all', action='store_true',
                          help='Run and show in an GUI window (all board)')

    cmdGroup.add_argument('--run_save', metavar='BOARDNAME',
                          help='Run and save as image file (single board)')

    cmdGroup.add_argument('--run_show', metavar='BOARDNAME',
                          help='Run and show in an GUI window (single board)')

    args = cmdArgsParser.parse_args()
    return args


if __name__ == '__main__':
    main()
