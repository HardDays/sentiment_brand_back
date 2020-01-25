from googleapiclient.discovery import build

import random

class GoogleSearch:

    def __init__(self, key, cx):
        self.cx = cx
        self.service = build("customsearch", "v1", developerKey=key)

    def search_social(self, query, social, pages=1):
        start = 1
        links = []
        dates = {}
        try:
            for i in range(0, pages):
                res = self.service.cse().list(q=query + ' site:' + social, start=start, cx=self.cx).execute()
                for link in res['items']:                        
                    date = None
                    try:
                        date_tokens = {'videoobject': 'uploaddate', 'newsarticle': 'datepublished', 'article': 'datepublished'}
                        for dt in date_tokens.keys():
                            if dt in link['pagemap'] and date_tokens[dt] in link['pagemap'][dt][0]:
                                date = link['pagemap'][dt][0][date_tokens[dt]][:10]
                    except Exception:
                        pass
                    links.append(link['link'])
                    if date:
                        dates[link['link']] = date
                start += 10
            return links, dates
        except Exception as ex:
            return links, dates

    def search(self, query, pages=1):
        sites = ['vk.com', 'instagram.com', 'facebook.com', 'ok.ru']
        links = []
        dates = {}
        for site in sites:
            res = self.search_social(query, site, pages=pages)
            links.extend(res[0])
            dates.update(res[1])
        random.shuffle(links)
        
        return links, dates
        