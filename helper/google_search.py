from googleapiclient.discovery import build

class GoogleSearch:

    def __init__(self, key, cx):
        self.cx = cx
        self.service = build("customsearch", "v1", developerKey=key)


    def search(self, query, pages=5):
        sites = query + ' site:vk.com OR site:instagram.com OR site:facebook.com OR site:ok.ru'
        start = 1
        links = []
        try:
            for i in range(0, pages):
                res = self.service.cse().list(q=sites, start=start, cx=self.cx).execute()
                for link in res['items']:
                    links.append(link['link'])
            return links
        except Exception as ex:
            print(ex)
            return links
        