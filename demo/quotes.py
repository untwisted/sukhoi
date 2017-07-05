"""

"""

from sukhoi import Miner, core, Pool

class AuthorMiner(Miner):
    def run(self, dom):
        elem = dom.fst('div', ('class', 'author-description'))
        self.pool.append(elem.text())

class QuoteMiner(Miner):
    def run(self, dom):
        elems = dom.find('div', ('class', 'quote'))
        self.pool.extend(map(self.extract_quote, elems))

        elem = dom.fst('li', ('class', 'next'))
        next_page = self.next(elem.fst('a').attr['href'])
        self.pool.append(QuoteMiner(next_page, self.pool))

    def extract_quote(self, elem):
        quote = elem.fst('span', ('class', 'text'))
        author_url = elem.fst('a').attr['href']

        return {'quote': quote.text(), 
        'author':AuthorMiner(self.next(author_url))}

if __name__ == '__main__':
    URL = 'http://quotes.toscrape.com/tag/humor/'
    pool = Pool()
    quotes = QuoteMiner(URL, pool)
    pool.append(quotes)
    core.gear.mainloop()

    print str(pool)

# { 'quote:' text
  # 'author': description }
