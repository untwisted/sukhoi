from sukhoi import MinerLXML, core

class AuthorMiner(MinerLXML):
    def run(self, dom):
        # The dom object is a struct returned by fromstring.
        # from lxml.html import fromstring
        # dom = fromstring(data)
        # See: http://lxml.de/tutorial.html
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





