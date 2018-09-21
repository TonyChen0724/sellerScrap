from bs4 import BeautifulSoup
import re

# Here is where we will begin scraping
pageNumber = 19

def page_url_produce(index):
    page1_url_prefix= "https://www.trademe.co.nz/stores/franklin-engineering-ltd/feedback?page="
    page1_url_extension = str(index)
    page1_url = page1_url_prefix + page1_url_extension
    return page1_url


def read_url(url):
    # This reads in a url and returns a BeautifulSoup
    # object. It also catches errors if something goes
    # wrong
    from urllib.request import urlopen
    from urllib.request import HTTPError
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        soup = BeautifulSoup(html.read(), "lxml")
    except AttributeError as e:
        print(e)
        return None
    return soup


def id_extract(page1_url):

    soup = read_url(page1_url)
    soup_content = soup.get_text()

    textfile = open('listIDHTMLPage.txt', 'w')
    textfile.write(soup_content)
    textfile.close()

    with open('listIDHTMLPage.txt') as f:
        ans = []
        for line in f:
            matches = re.findall(r'(?<!\w)(\#\w+)', line)
            ans.extend(matches)
        ans = ans[4:-1]

    return ans

sellIDList = []
for i in range(1, pageNumber):
    page1_url = page_url_produce(i)
    returnedList = id_extract(page1_url)
    sellIDList += returnedList

print(sellIDList)


