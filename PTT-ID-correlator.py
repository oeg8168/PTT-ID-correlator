import argparse


def parseArguments():
    cmdArgsParser = argparse.ArgumentParser()
    cmdGroup = cmdArgsParser.add_mutually_exclusive_group(required=True)

    cmdGroup.add_argument('--update', action='store_true',
                          help='Update database')

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


def main():
    args = parseArguments()


if __name__ == '__main__':
    main()
