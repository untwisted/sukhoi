from websnake import ResponseHandle, Get, Post
from ehp import Html as EhpHtml
import lxml.html as LxmlHtml
from bs4 import BeautifulSoup
from untwisted.core import die
from untwisted.task import Task, DONE
from urllib.parse import urlparse, urljoin
from untwisted.event import DESTROY
from untwisted import core
import cgi

default_headers = {
'user-agent':'Sukhoi/2.0.0', 
'connection': 'close'}

class Miner(list):
    task    = Task()
    task.add_map(DONE, lambda task: die())
    task.start()

    def __init__(self, url, headers=default_headers,  args={},
        method='get', payload={}, auth=()):

        self.url  = url
        self.auth = auth
        self.args = args

        self.urlparser = urlparse(url)
        self.encoding  = 'utf-8'
        self.response  = None
        self.headers   = headers
        self.payload   = payload
        self.method    = method

        super(list, self).__init__()
        self.next(self.url)

    def setup(self, response):
        # Reset the fd so it can be reread later.
        data = response.fd.read()
        response.fd.seek(0)

        type = response.headers.get('content-type', 
        'text/html; charset=%s' % self.encoding)

        # Sets the encoding for later usage
        # in self.geturl for example.
        params = cgi.parse_header(type)
        self.encoding = params[1]['charset']
        self.response = response

        data = data.decode(self.encoding, 'ignore')
        self.build_dom(data)

    def build_dom(self, data):
        pass

    def fetcher(self):
        request = Get(self.url, headers=self.headers, auth=self.auth)
        self.task.add(request.con, DESTROY)

        request.add_map(ResponseHandle.DONE, 
            lambda req, resp: self.setup(resp))
        return request

    def poster(self):
        request = Post(self.url, headers=self.headers, 
        payload=self.payload, auth=self.auth)

        self.task.add(request.con, DESTROY)
        request.add_map(ResponseHandle.DONE, 
            lambda req, resp: self.setup(resp))
        return request

    def geturl(self, reference):
        """
        """
        
        urlparser = urlparse(reference)

        if not urlparser.scheme:
            return urljoin('%s://%s' % (self.urlparser.scheme, 
                self.urlparser.hostname), reference) 
        return reference

    def next(self, reference):
        self.url = self.geturl(reference)
        self.urlparser = urlparse(self.url)

        if self.method == 'get':
            return self.fetcher()
        return self.poster()

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

