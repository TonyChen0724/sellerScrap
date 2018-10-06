from bs4 import BeautifulSoup
import re



def page_url_produce(url, index):
    page1_url_prefix = ""
    if "member" in url:

        if "page" not in url:
            page1_url_prefix = url + "&type=&page="

        else:
            splitedurlForMember = url.split('&')
            page1_url_prefix = splitedurlForMember[0] + "&" + splitedurlForMember[1] + "&page="

    else:
        if "page" not in url:
            page1_url_prefix = url + "?page="
        else:
            page1_url_prefix= url.split('=')[0] + "="
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

# (([0-3][0-9])|[0-9])/(([0-3][0-9])|[0-9])/[0-3][0-9]
def date_extract(page1_url):

    soup = read_url(page1_url)
    soup_content = soup.get_text()

    textfile = open('listIDHTMLPage.txt', 'w')
    textfile.write(soup_content)
    textfile.close()



    with open('listIDHTMLPage.txt') as f:
        ans = []
        for line in f:

            matches = re.findall(r'(([0-3][0-9])|[0-9])/(([0-3][0-9])|[0-9])/([0-3][0-9])', line)
            matches = list(matches)

            if (len(matches) != 0):
                while '' in matches:
                    matches.remove('')
                res = matches[0] + '/' + matches[1] + '/' + matches[2]   # how to convert turple to list

                ans.append(res)


    return ans


def gatherIDList(url, pageNumber):
    sellIDList = []
    sellDateList = []
    for i in range(1, pageNumber):
        page1_url = page_url_produce(url, i)
        returnedList = id_extract(page1_url)
        returneddate = date_extract(page1_url)
        sellIDList += returnedList
        sellDateList += returneddate

    print(len(sellIDList))
    print(len(sellDateList))
    return sellIDList

# gatherIDList(19)


