"""
This example extract just the quotes, you end up with a structure like:
    [quote0, quote1, ...]

Note: It uses beautifulsoup4 :)
"""

from sukhoi import MinerBS4, core

class QuoteMiner(MinerBS4):
    def run(self, dom):
        elems = dom.find_all('div', {'class':'quote'})
        self.extend(map(self.extract_quote, elems))

        elem = dom.find('li', {'class', 'next'})
        if elem: self.next(elem.find('a').get('href'))

    def extract_quote(self, elem):
        quote = elem.find('span', {'class': 'text'})
        return quote.text

if __name__ == '__main__':
    URL = 'http://quotes.toscrape.com/'
    quotes = QuoteMiner(URL)
    core.gear.mainloop()

    print quotes






