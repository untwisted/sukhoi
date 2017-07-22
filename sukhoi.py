from websnake import ResponseHandle, get, post
from ehp import Html as EhpHtml
import lxml.html as LxmlHtml
from bs4 import BeautifulSoup
from untwisted.iostd import LOST
from untwisted.core import die
from untwisted.task import Task, DONE
from urlparse import urlparse, urljoin
from untwisted import core
import cgi

HEADERS = {
'user-agent':'Sukhoi Web Crawler', 
'connection': 'close'}

class Fetcher(object):
    def __init__(self, miner):
        self.miner = miner
        con = get(self.miner.url, headers=self.miner.headers, 
        auth=self.miner.auth)

        self.install_handles(con)

    def install_handles(self, con):
        con.install_maps(('200', self.on_success), 
        ('302', self.on_redirect), 
        ('301', self.on_redirect))
        self.miner.task.add(con, LOST)

    def on_success(self, con, response):
        self.miner.setup(response)

    def on_redirect(self, con, response):
        con = get(response.headers['location'], 
        headers=self.miner.headers, auth=self.miner.auth)
        self.install_handles(con)

class Poster(Fetcher):
    def __init__(self, miner):
        self.miner = miner
        con = post(self.miner.url, 
        headers=self.miner.headers, payload=self.miner.payload,
        auth=self.miner.auth)

        self.install_handles(con)

    def on_redirect(self, con, response):
        con = post(response.headers['location'], 
        headers=self.miner.headers, payload=self.miner.payload, 
        auth=self.miner.auth)

        self.install_handles(con)

class Miner(list):
    task    = Task()
    task.add_map(DONE, lambda task: die())
    task.start()

    def __init__(self, url, pool=None, 
        headers=HEADERS, method='get', payload={}, auth=()):
        self.pool      = pool
        self.url       = url
        self.urlparser = urlparse(url)
        self.headers   = headers
        self.method    = method
        self.payload   = payload
        self.auth      = auth
        self.encoding  = 'utf-8'
        self.response  = None

        super(list, self).__init__()
        self.expand()

    def expand(self):
        """
        No exception being raised.
        """
        try:
            self.create_connection()
        except Exception as excpt:
            print excpt

    def setup(self, response):
        data = response.fd.read()
        
        # Reset the fd so it can be reread later.
        response.fd.seek(0)

        type = response.headers.get('content-type', 
        'text/html; charset=%s' % self.encoding)

        params = cgi.parse_header(type)

        # Sets the encoding for later usage
        # in self.geturl for example.
        self.encoding = params[1]['charset']
        self.response = response
        data          = data.decode(self.encoding, 'ignore')
        self.build_dom(data)

    def build_dom(self, data):
        pass

    def create_connection(self):
        if self.method == 'get':
            return Fetcher(self) 
        return Poster(self)

    def geturl(self, reference):
        """
        """
        
        # It is necessary to encode back the url
        # because websnake get method inserts the host header
        # with the wrong encoding and some web servers wouldnt
        # accept it as valid header.
        reference = reference.encode(self.encoding)
        urlparser = urlparse(reference)
        url       = urljoin('%s://%s' % (self.urlparser.scheme, 
        self.urlparser.hostname), reference) \
        if not urlparser.scheme else reference
        return url

    def next(self, reference):
        self.url       = self.geturl(reference)
        self.urlparser = urlparse(self.url)
        self.expand()

    def run(self, dom):
        """
        Implement your rules here.
        """

        pass

class MinerEHP(Miner):
    """
    Use EHP to build the dom structure.
    """

    html = EhpHtml()

    def build_dom(self, data):
        dom  = self.html.feed(data)
        self.run(dom)

class MinerLXML(Miner):
    """
    Use lxml to build the structure.
    """

    def build_dom(self, data):
        dom = LxmlHtml.fromstring(data)
        self.run(dom)

class MinerBS4(Miner):
    """
    Use lxml parser with beautifulsoup4.
    """

    def build_dom(self, data):
        dom = BeautifulSoup(data, 'lxml')
        self.run(dom)



