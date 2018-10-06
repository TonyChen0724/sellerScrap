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
    # global percentile_list
    testList = gatherIDList(url, int(pageNum))
    page1_url_prefix = "https://www.trademe.co.nz/"
    productNames = []
    productPrices = []
    page_urls = []
    productClosingTimes = []

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
            productPrice = soup.find("div", {"id": "BuyNow_BuyNow"}).get_text().replace('$', '').replace(',', '')
            if productPrice != "noPrice":
                productPrice = float(productPrice)
            else:
                productPrice = -1.0
            productPrices.append(productPrice)
            print(productPrice)

        except AttributeError as e:
            try:
                productPrice = soup.find("div", {"id": "Bidding_CurrentBidValue"}).get_text().replace('$', '').replace(',', '')
                productPrices.append(float(productPrice))
                print(productPrice)
                print("noPrice-" + productPrice)
            except AttributeError as e:
                productPrices.append("noPrice")
                print("noPrice")

        # try:
        #     productClosingTime = soup.find("div", {"id": "ClosingTime_ClosingTime"}).get_text()


        try:
            productClosingTime = soup.find("span", {"id": "ClosingTime_ClosingTime"}).get_text()
            productClosingTimes.append(productClosingTime)
            print(productClosingTime)
        except AttributeError as e:
            print("noTime")
            productClosingTimes.append("noTime")


        print("----------------------------------------------------")

    import pandas as pd

    try:
        percentile_list = pd.DataFrame(
            {'productName': productNames,
             'productPrice': productPrices,
             'productClosingTime': productClosingTimes,
             'page_urls': page_urls
            })
    except ValueError:
        pass

    print(percentile_list)
    productFrequency = percentile_list.productName.value_counts()

    values = productFrequency.keys().tolist()
    counts = productFrequency.tolist()
    frequencyPrices = [percentile_list.loc[percentile_list['productName'] == s, 'productPrice'].iloc[0] for s in values]
    frequencyClosingTime = [percentile_list.loc[percentile_list['productName'] == s, 'productClosingTime'].iloc[0] for s in values]
    frequencyPrices = [float(_) for _ in frequencyPrices]
    frequencyURL = [percentile_list.loc[percentile_list['productName'] == s, 'page_urls'].iloc[0] for s in values]

    quantityToplist = pd.DataFrame(
        {'productName': values,
         'productsold': counts,
         'productprices': frequencyPrices,
         'closingTime': frequencyClosingTime,
         'product_url': frequencyURL

         })

    quantityToplist.to_csv(sellerName + "quantityTopList.csv")
    counts = [float(_) for _ in counts]

    from itertools import zip_longest
    product_volumn = [x * y for x, y in (zip_longest(frequencyPrices, counts, fillvalue=1))]

    volumnTopList = pd.DataFrame(
        {'productName': values,
         'productQuantity': counts,
         'productPrice': frequencyPrices,
         'productVolumn': product_volumn,
         'closingTime': frequencyClosingTime,
         'product_url': frequencyURL
         })

    volumnTopList = volumnTopList.sort_values(by=['productVolumn'], ascending=False)


    volumnTopList.to_csv(sellerName + "volumnTopList.csv")

    percentile_list.to_csv(sellerName + ".csv")







