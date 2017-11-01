#! /bin/env python

## LOL

import argparse
import os.path
import pandas as pd


def main(argv=sys.argv):
    arg_parser = argparse.ArgumentParser(description=prog_descrip)
    arg_parser.add_argument('-c','--csv_file', nargs='?', action='store', required=True, type=os.path.abspath,
                            help=('Path to ptseries .csv FILE. (/PATH/TO/exported.csv)'),
                            dest='csv_file'
                           )
    args = arg_parser.parse_args()

csv = pd.read_csv(args.csv_file)

csv = csv.T

csv.to_csv(os.path.join(args.csv_file), index=False)