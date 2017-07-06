# Sukhoi

Minimalist and powerful Web Crawler.

# Features

- **Http/https support**

- **Short learning curve**

- **Extremely fast compared to other crawlers**

### Basic example

~~~python

from sukhoi import Miner, core

class AuthorMiner(Miner):
    def run(self, dom):
        elem = dom.fst('div', ('class', 'author-description'))
        self.pool.append(elem.text().strip().rstrip())

class QuoteMiner(Miner):
    def run(self, dom):
        elems = dom.find('div', ('class', 'quote'))
        self.pool.extend(map(self.extract_quote, elems))

        elem = dom.fst('li', ('class', 'next'))
        if elem: self.next(elem.fst('a').attr['href'])

    def extract_quote(self, elem):
        quote = elem.fst('span', ('class', 'text'))
        author_url = elem.fst('a').attr['href']

        return {'quote': quote.text().strip().rstrip(), 
        'author':AuthorMiner(self.geturl(author_url))}

if __name__ == '__main__':
    URL = 'http://quotes.toscrape.com/tag/humor/'
    quotes = QuoteMiner(URL)
    core.gear.mainloop()

    print repr(quotes.pool)
~~~

The above code would output a json structure like:

~~~
[{'quote': 'The quote extracted.', 
'Author': 'The autor description from the about link.'}, ...]
~~~

Notice the above code differs slightly from main scrapy example because it catches not just
the name of the author but the complete description of the author thats found from
the link whose text is "about".

Sukhoi is built on top of [EHP](https://github.com/iogf/ehp) which is a very robust ast builder or HTML.
It is still in its baby ages i hope it grows strong and useful.

# Documenntation

[Wiki](https://github.com/iogf/sukhoi/wiki)

