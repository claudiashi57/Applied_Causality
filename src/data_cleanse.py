from ast import literal_eval
import numpy as np
import pandas as pd

dir_path = '/Users/claudiashi/Dropbox/Unpopulareconideas/data/csv/'
def load_data(year=1960, dir_path=dir_path):
    file_path = dir_path + str(year) + ".csv"
    df = pd.read_csv(file_path, delimiter=",")
    return df


def delete_rows(df):
    df = df[df.authors != '[]']
    df = df[df.journal != 'Challenge']
    df = df[df.journal != 'Quarterly Banking Review / רבעון לבנקאות']
    df = df[df.journal != 'The Economic Quarterly / הרבעון לכלכלה']
    return df


def clearn_author(df):
    df.authors = [elem.replace("[", "").replace("]", "") for elem in df.authors.values]
    df.authors = [elem.replace("'", "").replace("'", "") for elem in df.authors]
    return df

def clean_cites(df):
    df.all_cites = [literal_eval(elem) for elem in df.all_cites]
    df.all_cites=[[elem.replace("\n", "") for elem in df.all_cites[idx]] for idx in df.index]
    return df




if __name__ == '__main__':
    for i in range(59):
        year = 1960 + 1
        df = load_data(year, dir_path)
        df = delete_rows(df)
        df = clearn_author(df)
        df = clean_cites(df)


