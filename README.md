# Sukhoi

Minimalist and powerful Web Crawler.

Sukhoi is built on top of the concept of miners, it is similar to what happens with scrapy and its spiders.
However, in sukhoi the miners can be placed in structures like lists or dictionaries in order to 
construct json-like structures for the data thats extracted from the pages.

# Features

- **Http/https support**

- **Short learning curve**

- **Extremely fast**

- **GET/POST requests**

- **Basic AUTH support**

- **Modular**

- **Support for LXML**

- **Non-blocking I/O**

### Basic example

The basic example below is equivalent to scrapy's main example although it not only scrapes the author's name
but its complete description that stays a layer down from the quotes's pages.

Miners inherit from python list class, so they can be used to accumulate data from the pages, they can be placed anywhere too(in this way
it is highly flexible to construct json structures for your fetched data.)

~~~python
from sukhoi import MinerLXML, core

class AuthorMiner(MinerLXML):
    def run(self, dom):
        # Grab the text for the author description
        # and accumulate it.
        elems = dom.xpath("//div[@class='author-description']")
        self.append(elems[0].text)

class QuoteMiner(MinerLXML):
    def run(self, dom):
        # Grab all the quotes.
        elems = dom.xpath("//div[@class='quote']")
        self.extend(map(self.extract_quote, elems))

        # Grab the link that points to the next page.
        next_page = dom.xpath("//li[@class='next']/a[@href][1]")
        
        # If there is a next page then flies there to extract
        # the quotes.
        if next_page: self.next(next_page[0].get('href'))

    def extract_quote(self, elem):
        # Grab the quote text.
        quote = elem.xpath(".//span[@class='text']")[0].text

        # Grab the url description.
        author_url = elem.xpath(".//a[@href][1]")[0].get('href')

        # Return the desired structure, and tells AuthorMiner to fly
        # to the url that contains the author description.
        return {'quote': quote, 
        'author':AuthorMiner(self.geturl(author_url))}


if __name__ == '__main__':
    URL = 'http://quotes.toscrape.com/'
    quotes = QuoteMiner(URL)
    core.gear.mainloop()

    # As miners inherit from lists, you end up with
    # the desired structure containg the quotes and the
    # author descriptions.
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

You can use either [EHP](https://github.com/iogf/ehp) or [lxml](http://lxml.de/) with sukhoi.

Sukhoi permits one to split up the parsing into miners in a succint way that permits clean and consistent code.
Miners can receive pool objects that are used to accurately construct the desired data structure. 

The example below scrapes all the tags from http://quotes.toscrape.com/ by following pagination 
then makes sure they are unique then scrapes all the quotes from them with their author description.
The example below uses EHP to extract the data from the htmls.

~~~python
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

class TagMiner(MinerEHP):
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









