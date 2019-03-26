from ast import literal_eval
import numpy as np
import pandas as pd

dir_path = '/Users/claudiashi/Dropbox/Unpopulareconideas/data/all_csv/csv/'
save_path = '/Users/claudiashi/Dropbox/Unpopulareconideas/data/all_csv/csv_top5/'
def load_data(year=1960, dir_path=dir_path):
    file_path = dir_path + str(year) + ".csv"
    df = pd.read_csv(file_path, delimiter=",")
    return df

approved_list=['Journal of Political Economy','Econometrica', 'The Quarterly Journal of Economics'
'The American Economic Review','The Review of Economic Studies']

def clean_duplicate(df):
    df = df.sort_values('length', ascending=False)
    df = df.drop_duplicates(['article'])
    return df


def delete_rows(df):
    df = df[df.authors != '[]']
    df = df[df['journal'].isin(approved_list)]

    df = df[df['article'].map(len) > 10]
    return df


def clearn_author(df):
    df.authors = [elem.replace("[", "").replace("]", "") for elem in df.authors.values]
    df.authors = [elem.replace("'", "").replace("'", "") for elem in df.authors]
    return df

def clean_cites(df):
    df.all_cites = [literal_eval(elem) for elem in df.all_cites]
    df.all_cites=[[elem.replace("\n", "") for elem in df.all_cites[idx]] for idx in df.index]
    return df



def main(year):

    df = load_data(year, dir_path)
    df = delete_rows(df)
    df = clearn_author(df)
    df = clean_duplicate(df)
    df.to_csv(save_path + '{}.csv'.format(year))
    print("the length of the file is: ", len(df.authors))
    return df

def get_all_author():
    authors = []
    filename = '/Users/claudiashi/ml/Applied_Causality/logging.txt'
    for i in range(2):
        print("i is: ", i)
        year = 1960 + i
        df = main(year)
        authors.append(np.unique(df.authors))
    all_author= np.concatenate(authors)
    var=np.unique(all_author)
    print(type(var))
    var.tofile(filename, sep=" ")



if __name__ == '__main__':
    counter = 0
    for i in range(59):
        year = 1960 + i
        print("year is, ", year)
        main(year)


#get_all_author()
