import argparse
from collections import namedtuple, Counter

import numpy as np
import pandas as pd


def replace_missing_list_column_values(df, col_name):
    """Replace nans with empty list in list type columns

        * Features such as genres, awards, characters etc are of type 'list'.
        * The default value for missing values for these columns should be an
          empty list instead of nan/None
        * We cannot use fillna() since it does not accept a list as a value

        Mutates the dataframe in place.
    """
    missing_values = df[col_name].isnull()
    df.loc[missing_values, col_name] = pd.Series(
        [
            [] for _ in range(missing_values.count())
        ])



###################################
######### For script mode #########
###################################

def parse_args():
    parser = argparse.ArgumentParser(description='Aggregator script to clean and transform Goodreads data')
    parser.add_argument('-f', '--filenames', nargs='+', help='Space separated JSONLINES files extracted from Goodreads', required=True)
    parser.add_argument('-o', '--output', help='Output CSV file name to which data will be extracted', required=True)
    return parser.parse_args()

def main():
    args = parse_args()

    dfs = [pd.read_json(filename, lines=True) for filename in args.filenames]
    df = pd.concat(dfs)
    df = df.drop_duplicates(subset=['url'])

    replace_missing_list_column_values(df, 'genres')



    print(df.head())

    df.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
