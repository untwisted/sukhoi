from ehp import Html
from websnake import ResponseHandle, get
from untwisted.iostd import CLOSE, LOST, CONNECT_ERR
from untwisted.core import die
from untwisted.task import Task, DONE
from urlparse import urlparse, urljoin
from untwisted import core

HEADERS = {
'user-agent':'Sukhoi Web Crawler', 
'connection': 'close'}

class Fetcher(object):
    def __init__(self, miner, url):
        self.miner = miner
        self.url  = url

        con = get(url, headers=self.miner.headers)
        self.install_handles(con)

    def install_handles(self, con):
        con.install_maps(('200', self.on_success), 
        ('302', self.on_redirect), 
        ('301', self.on_redirect))
        self.miner.task.add(con, LOST)

    def on_success(self, con, response):
        dom = self.miner.html.feed(response.fd.read())
        self.miner.run(dom)

    def on_redirect(self, con, response):
        con = get(response.headers['location'], 
        headers=self.miner.headers)
        self.install_handles(con)

class Miner(object):
    html    = Html()
    visited = set()
    task    = Task()
    task.add_map(DONE, lambda task: die())
    task.start()

    def __init__(self, url, pool=None, max_depth=10, headers=HEADERS):
        self.pool      = pool if pool != None else []
        self.url       = url
        self.urlparser = urlparse(url)
        self.max_depth = max_depth
        self.headers   = headers

        try:
            fetcher = Fetcher(self, self.url)
        except Exception as excpt:
            print excpt

    def geturl(self, reference):
        urlparser = urlparse(reference)
        url       = urljoin('%s://%s' % (self.urlparser.scheme, 
        self.urlparser.hostname), reference) \
        if not urlparser.scheme else reference
        return url

    def next(self, reference):
        url = self.geturl(reference)
        self.__class__(url, self.pool, self.max_depth)

    def __repr__(self):
        return str(self.pool)

    def run(self, dom):
        """
        """

        pass


