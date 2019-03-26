from data_cleanse import *
import regex
dir_path = '/Users/claudiashi/Dropbox/Unpopulareconideas/data/all_csv/csv_top5/'
save_path = '/Users/claudiashi/Dropbox/Unpopulareconideas/data/all_csv/csv_cite/'
def letter_only(string):
    return ''.join(e for e in string if e.isalnum()).lower()


def smash_citations(df):
    x = "".join(df.all_cites.values.astype('str'))
    return letter_only(x)

def get_citation(yr):
    df = load_data(yr, dir_path=dir_path)
    cite_that_year = np.zeros(df.shape[0])
    future = 2009 - yr
    for i in range(future):
        print("I am at year: ", i)
        year = yr + i +1
        df_year = load_data(year, dir_path)
        all_cites = smash_citations(df_year)
        for j in range(len(cite_that_year)):
            paper = letter_only(df.article[j])
            cite_that_year[j] = len(regex.findall(paper, all_cites))
        df[str(year)] = cite_that_year
    return df



def main():
    for i in range(49):
        yr = i + 1960
        print(" I am handling the data for: ", yr)
        df = get_citation(yr)
        df.to_csv(save_path + '{}.csv'.format(year))



