import requests
from bs4 import BeautifulSoup



class mirror:
    domain = 'demo.en.cx'
    headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
                }

    def __init__(self):
        pass


    def set_url(self, in_url):
        self.domain = in_url

    def print_domain(self):
        return self.domain

    def get_url(self):
        if self.domain.find('http://') != -1 :
            page = requests.get(self.domain, headers=self.headers)
            return page.text.encode(page.encoding)
        else:
            self.set_url('http://'+self.domain)
            page = requests.get(self.domain, headers=self.headers)
            return page.text.encode(page.encoding)

    def print_tags(self):
        soup = BeautifulSoup(self.get_url(), 'lxml')
        print(soup.prettify().encode('utf8'))
