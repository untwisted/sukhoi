from ehp import Html
from websnake import ResponseHandle, get
from untwisted.iostd import CLOSE, LOST, CONNECT_ERR
from untwisted.core import die
from untwisted.task import Task, DONE
from urlparse import urlparse, urljoin
from untwisted import core

class Pool(list):
    pass

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
    headers = {
    'user-agent':'Sukhoi Web Crawler', 
    'connection': 'close'}
    html    = Html()
    visited = set()
    task    = Task()
    task.add_map(DONE, lambda task: die())

    def __init__(self, url, pool=None, max_depth=10):
        self.pool = pool if pool != None else []
        self.url       = url
        self.urlparser = urlparse(url)
        self.max_depth = max_depth

        try:
            Fetcher(self, url)
        except Exception as e:
            print e, url
        else:
            self.task.start()

    def run(self, dom):
        pass

    def next(self, url):
        urlparser = urlparse(url)
        tmp = urljoin('%s://%s' % (self.urlparser.scheme, 
        self.urlparser.hostname), url) \
        if not urlparser.scheme else url
        return tmp

    def __repr__(self):
        return str(self.pool)

    def __str__(self):
        return str(self.pool)


