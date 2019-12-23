from googleapiclient.discovery import build

class GoogleSearch:

    def __init__(self, key, cx):
        self.cx = cx
        self.service = build("customsearch", "v1", developerKey=key)


    def search_social(self, query, social, pages=1):
        start = 1
        links = []
        try:
            for i in range(0, pages):
                res = self.service.cse().list(q=query + ' site:' + social, start=start, cx=self.cx).execute()
                for link in res['items']:
                    links.append(link['link'])
                start += 10
            return links
        except Exception as ex:
            print(ex)
            return links
         

    def search(self, query, pages=1):
        sites = ['vk.com', 'instagram.com', 'facebook.com', 'ok.ru']
        links = []
        for site in sites:
            res = self.search_social(query, site, pages=pages)
            links.extend(res)
        return links
        