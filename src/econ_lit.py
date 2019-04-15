from data_cleanse import *
from fuzzywuzzy import fuzz
from utils import *
def drop_data(df):
    df = df[['Title', 'Authors', 'correspondenceAuthor', 'pubdate', 'pubtitle', 'year', 'pages', 'subjectTerms']]
    return df


def add_features(jstor, econlit):
    tags = np.empty(jstor.article.shape, dtype='<U1000')
    corr_author = np.empty(jstor.article.shape, dtype='<U100')
    all_author = np.empty(jstor.article.shape, dtype='<U1000')
    for i in range(len(jstor.article)):
        found_match = False
        for j in range(len(econlit.Title)):
            a = letter_only(jstor.article[i])
            b = letter_only(econlit.Title.values[j])
            if fuzz.ratio(a, b) > 90 and found_match == False:
                found_match = True
                print(i)
                tags[i] = econlit.subjectTerms.values[j]
                corr_author[i] = econlit.correspondenceAuthor.values[j]
                all_author[i] = econlit.Authors.values[j]
        if found_match == False:
            print(i)
            tags[i] = 'None'
            corr_author[i] = 'None'
            all_author[i] = 'None'

    jstor['all_author'] = all_author
    jstor['tags'] = tags
    jstor['corr_author'] = corr_author

    return jstor

