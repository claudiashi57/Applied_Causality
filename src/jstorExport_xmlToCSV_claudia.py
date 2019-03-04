from bs4 import BeautifulSoup
import os
import csv

#file_root = "./economics_journals_1960/"
#save_file = "./1960.csv"
file_root = "/Users/claudiashi/Dropbox/Unpopulareconideas/data/jstorExport/economics_journals_1960/"
save_file = "/Users/claudiashi/Dropbox/Unpopulareconideas/data/claudia/1960.csv"


def get_row(path):
    """
    get_row extracts the values out of an xml file, into an arraw which is what the csv_writer expects
    if we find ourselves wanting to change the structure of the csv, we can return a data class rather than
    an array and let xml_to_csv handle deciding the row order. 
    
    Arguments:
        path: location of xml file
    
    Returns:
        [] if the row should not be written
        array in the format of ['article','journal','month','year','authors','length','abstract']
    """
    with open(path) as f:
        soup = BeautifulSoup(f.read(), 'xml')

        # There is an article-type tag as an attribute in the root of the xml. This would be better
        # to filter on, but it's not immediately clear how to get the data in beautiful soup. Although
        # it's probably possible
        if not soup.find('article-title'):
            return []

        # some types have no article but still include a blank title name
        if not soup.find('article-title').get_text():
            return []
            
        article_title = soup.find('article-title').get_text()
        journal_title = soup.find('journal-title').get_text()

        pub_date = soup.find('pub-date')
        month = pub_date.month.get_text()
        year = pub_date.year.get_text()

        article_len = ""
        if soup.find('lpage') and soup.find('fpage') and str.isnumeric(soup.find('lpage').get_text()) and str.isnumeric(soup.find('fpage').get_text()):
            article_len = str(int(soup.find('lpage').get_text()) - int(soup.find('fpage').get_text()))

        contributors = []
        for contributor in soup.find_all('string-name'):
            # Some contributor tags are blank, so we skip them
            if contributor.find('given-names') and contributor.find('surname'):
                fn = contributor.find('given-names').get_text()
                ln = contributor.find('surname').get_text()
                contributors.append("{},{}".format(ln, fn))
        
        abstract = soup.find('abstract')

        return [article_title, journal_title, month, year, contributors, article_len, abstract]


def xml_to_csv(save_file, file_root):
    """
    xml_to_csv extracts relevant information out of the XML file and
    writes it to csv. All data that does not have a corresponding value in the xml will 
    be written as a blank string to the csv file.
    """
    with open(save_file, 'w',newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        head =['article','journal','month','year','authors','length','abstract']
        writer.writerow(head)
        for xml_file in os.listdir(file_root): 
            row = get_row(os.path.join(file_root, xml_file))
            if row:
                writer.writerow(row)


def main():
    file_root =  "/Users/claudiashi/Dropbox/Unpopulareconideas/data/jstorExport/economics_journals_1960/"
    save_file = "/Users/claudiashi/Dropbox/Unpopulareconideas/data/claudia/1960.csv"

    xml_to_csv(save_file, file_root)


main()