from spyre import server
import pandas as pd

import US_keywords, UK_keywords, DE_keywords, FR_keywords, IT_keywords, ES_keywords, JP_keywords


class Keywords(server.App):
    title = 'Search For Keywords'

    countries = [
        {'label': 'US', 'value': 'US'},
        {'label': 'UK', 'value': 'UK'},
        {'label': 'DE', 'value': 'DE'},
        {'label': 'JP', 'value': 'JP'},
        {'label': 'FR', 'value': 'FR'},
        {'label': 'IT', 'value': 'IT'},
        {'label': 'ES', 'value': 'ES'}
    ]

    inputs = [
        {
            'type': 'dropdown',
            'label': 'Country',
            'options': countries,
            'key': 'country',
        },
        {
            'type': 'text',
            'key': 'search',
            'label': 'search term',
        },
        {
            'type': 'text',
            'label': 'negative',
            'key': 'negative',
        }
    ]

    controls = [
        {
            'type': 'button',
            'label': 'Search',
            'id': 'update_search'
    }
    ]

    tabs = ['Search Result']

    outputs = [
        {
            'type': 'table',
            'id': 'table',
            'control_id': 'update_search',
            'tab': 'Search Result',
        }
    ]

    def getData(self, params):
        country = params['country']
        search = params['search']
        negative = str(params['negative']).split(',')

        if country == 'US':
            kw_lst = US_keywords.kw_scrape(search)
        elif country == 'UK':
            kw_lst = UK_keywords.kw_scrape(search)
        elif country == 'DE':
            kw_lst = DE_keywords.kw_scrape(search)
        elif country == 'FR':
            kw_lst = FR_keywords.kw_scrape(search)
        elif country == 'IT':
            kw_lst = IT_keywords.kw_scrape(search)
        elif country == 'ES':
            kw_lst = ES_keywords.kw_scrape(search)
        elif country == 'JP':
            kw_lst = JP_keywords.kw_scrape(search)

        if 'kw_lst' in locals():
            if len(kw_lst) > 0:
                df = pd.DataFrame(kw_lst, columns=['Keyword'])
                df.drop_duplicates(inplace=True)
                if negative != ['']:
                    for ele in negative:
                        df = df[~df.Keyword.str.contains(str(ele))]
                    df.index = range(df.shape[0])
                    df['Negative'] = pd.Series(negative)
        return df

app = Keywords()
app.launch(host='0.0.0.0',port=8000)
