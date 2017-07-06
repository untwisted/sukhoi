# Sukhoi

Minimalist and powerful Web Crawler.

Sukhoi is built on top of the concept of miners, it is similar to what happens with scrapy and its spiders.
However, in sukhoi the miners are responsible by fetching html either through get/post requests. 
They can be placed in structures like lists or dictionaries in order to construct json-like structures
for the data thats extracted from the pages.

# Features

- **Http/https support**

- **Short learning curve**

- **Extremely fast**

- **GET/POST requests**

- **Basic AUTH support**

- **Modular**

### Basic example

The basic example below is equivalent to scrapy's main example although it not only scrapes the author's name
but its complete description that stays a layer down from the quotes's pages.

Miners inherit from python list class, so they can be used to accumulate data from the pages, they can be placed anywhere too(in this way
it is highly flexible to construct json structures for your fetched data.)

~~~python
from sukhoi import Miner, core

class AuthorMiner(Miner):
    def run(self, dom):
        elem = dom.fst('div', ('class', 'author-description'))
        self.append(elem.text())

class QuoteMiner(Miner):
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

~~~

The above code would output a json structure like:

~~~
[{'quote': 'The quote extracted.', 
'author': 'The autor description from the about link.'}, ...]
~~~

Notice the above code differs slightly from main scrapy example because it catches not just
the name of the author but the complete description of the author thats found from
the link whose text is "about".

Sukhoi is built on top of [EHP](https://github.com/iogf/ehp) which is a very robust ast builder or HTML.
It is still in its baby ages i hope it grows strong and useful.

Sukhoi permits one to split up the parsing into miners in a succint way that permits clean and consistent code.
Miners can receive pool objects that are used to accurately construct the desired data structure. 

The example below scrapes all the tags from http://quotes.toscrape.com/ by following pagination
then makes sure they are unique then scrapes all the quotes from them with their author description.

~~~python

from sukhoi import Miner, core

class AuthorMiner(Miner):
    def run(self, dom):
        elem = dom.fst('div', ('class', 'author-description'))
        self.append(elem.text())

class QuoteMiner(Miner):
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

class TagMiner(Miner):
    acc = set()

    def run(self, dom):
        tags = dom.find('a', ('class', 'tag'))

        self.acc.update(map(lambda ind: (ind.text(), 
        ind.attr['href']), tags))

        elem = dom.fst('li', ('class', 'next'))

        if elem: 
            self.next(elem.fst('a').attr['href'])
        else: 
            self.extract_quotes()
            
    def extract_quotes(self):
        self.extend(map(lambda ind: (ind[0], 
        QuoteMiner(self.geturl(ind[1]))), self.acc))

if __name__ == '__main__':
    URL = 'http://quotes.toscrape.com/'
    tags = TagMiner(URL)
    core.gear.mainloop()

    print tags
~~~

The structure would look like:

~~~
[(tag_name, {'quote': 'The quote text.', 'author': "The author description from the about link'}), ...]
~~~

# Install

~~~
pip2 install -r requirements.txt
pip2 install sukhoi
~~~

# Documenntation

[Wiki](https://github.com/iogf/sukhoi/wiki)






