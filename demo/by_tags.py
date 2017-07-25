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

        elem = dom.fst('li', ('class', 'next'))
        if elem: self.next(elem.fst('a').attr['href'])

    def extract_quote(self, elem):
        quote = elem.fst('span', ('class', 'text'))
        author_url = elem.fst('a').attr['href']

        return {'quote': quote.text(), 
        'author':AuthorMiner(self.geturl(author_url))}

class TagMiner(MinerEHP):
    acc = set()

    def run(self, dom):
        tags = dom.find('a', ('class', 'tag'))

        self.acc.update([(ind.text(), 
        ind.attr['href']) for ind in tags])

        elem = dom.fst('li', ('class', 'next'))

        if elem: 
            self.next(elem.fst('a').attr['href'])
        else: 
            self.extract_quotes()
            
    def extract_quotes(self):
        self.extend([(ind[0], 
        QuoteMiner(self.geturl(ind[1]))) for ind in self.acc])

if __name__ == '__main__':
    URL = 'http://quotes.toscrape.com/'
    tags = TagMiner(URL)
    core.gear.mainloop()

    print(tags)





