import requests
import pandas as pd

d = {}
n = 0
searched = []


def drop_down(search):
    global n
    global d
    global searched
    search = search.replace(' ', '%20')
    url = 'https://completion.amazon.co.uk/search/complete?mkt=4&search-alias=aps&q=' + search
    wb_data = requests.get(url)
    d[n] = [ele.replace('"', '') for ele in wb_data.text.split(',[')[1].split(',')]
    d[n] = [ele.replace(']', '') for ele in d[n]]
    searched.append(search.replace('%20', ' '))
    for kw in [ele for ele in d[0]]:    # base case 1: if search term == response
        if (kw not in searched) and (len(kw.split()) < 4):
            n += 1
            drop_down(kw)


def kw_scrape(search):
    global n
    global d
    global searched
    drop_down(search)
    kw_lst = []
    for ele in d.keys():
        kw_lst.extend(d[ele])
    d = {}
    n = 0
    searched = []
    # kw = pd.DataFrame(kw_lst, columns=['Keyword'])
    # kw.drop_duplicates(inplace=True)
    return kw_lst
