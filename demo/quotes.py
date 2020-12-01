"""

"""

from sukhoi import MinerEHP, core

class AuthorMiner(MinerEHP):
    def run(self, dom):
        elem = dom.fst('div', ('class', 'author-description'))
        self.append(elem.text())

class QuoteMiner(MinerEHP):
    def run(self, dom):
        elems = dom.find('div', ('class', 'quote'))
        self.extend(list(map(self.extract_quote, elems)))

        next_page = dom.fst('li', ('class', 'next'))
        if next_page: 
            self.next(next_page.fst('a').attr['href'])
        # When there is a next page just fetches using
        # the same miner.

    def extract_quote(self, elem):
        quote = elem.fst('span', ('class', 'text'))
        author_url = elem.fst('a').attr['href']
        author_url = self.geturl(author_url)

        return {'quote': quote.text(), 
        'author':AuthorMiner(author_url)}

if __name__ == '__main__':
    URL = 'http://quotes.toscrape.com/tag/humor/'
    quotes = QuoteMiner(URL)
    core.gear.mainloop()
    print(quotes)
