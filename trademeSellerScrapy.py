from bs4 import BeautifulSoup
from listIDgathering import *



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

# Here is where we will begin scraping


def startMakingCSV(url, pageNum, sellerName):
    testList = gatherIDList(url, int(pageNum))
    page1_url_prefix = "https://www.trademe.co.nz/"
    productNames = []
    productPrices = []
    page_urls = []

    for listID in testList:
        appendix = listID[1:]
        page1_url = page1_url_prefix + appendix
        print(page1_url)
        soup = read_url(page1_url)

        if (soup == None):
            continue


        page_urls.append(page1_url)
        try:
            productName = soup.find("div", {"id" : "ListingTitleBox_TitleText"}).get_text()
            productNames.append(productName)
            print(productName)
        except AttributeError as e:
            print("noName")
            productNames.append("noName")

        try:
            productPrice = soup.find("div", {"id": "BuyNow_BuyNow"}).get_text()
            productPrices.append(productPrice)
            print(productPrice)

        except AttributeError as e:
            try:
                productPrice = soup.find("div", {"id": "Bidding_CurrentBidValue"}).get_text()
                productPrices.append(productPrice)
                print(productPrice)
                print("noPrice-" + productPrice)
            except AttributeError as e:
                productPrices.append("noPrice")
                print("noPrice")


        print("----------------------------------------------------")

    import pandas as pd

    try:
        percentile_list = pd.DataFrame(
            {'productName': productNames,
            'productPrice': productPrices,
             'page_urls': page_urls
            })
    except ValueError:
        pass

    print(len(productNames))
    print(len(productPrices))

    percentile_list.to_csv(sellerName)







