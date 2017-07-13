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
        self.extend(map(self.extract_quote, elems))

        elem = dom.fst('li', ('class', 'next'))
        if elem: self.next(elem.fst('a').attr['href'])

    def extract_quote(self, elem):
        quote = elem.fst('span', ('class', 'text'))
        author_url = elem.fst('a').attr['href']

        return {'quote': quote.text(), 
        'author':AuthorMiner(self.geturl(author_url))}

if __name__ == '__main__':
    URL = 'http://quotes.toscrape.com/tag/humor/'
    quotes = QuoteMiner(URL)
    core.gear.mainloop()

    print quotes



