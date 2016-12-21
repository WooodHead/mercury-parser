import requests
import maya

MERCURY_API = 'https://mercury.postlight.com/parser?url='

class ParsedArticle(object):
    """docstring for ParsedArticle"""
    def __init__(self, parser):
        super(ParsedArticle, self).__init__()
        self._parser = parser

        self.title = None
        self.content = None
        self.date_published = None
        self.lead_image_url = None
        self.dek = None
        self.url = None
        self.domain = None
        self.excerpt = None
        self.word_count = None
        self.direction = None
        self.total_pages = None
        self.rendered_pages = None
        self.next_page_url = None

    def __repr__(self):
        return '<ParsedArticle url={0!r}>'.format(self.url)

    @classmethod
    def from_dict(klass, d, parser):

        # The new ParsedArticle.
        p = klass(parser=parser)

        # Add all values from returned JSON object to instance.
        for key, value in d.iteritems():
            setattr(p, key, value)

        # Proper Datetimes.
        p.date_published = maya.MayaDT.from_iso8601(p.date_published).datetime()

        return p

    def next(self):
        if self.next_page_url:
            return self._parser.parse(self.next_page_url)


class ParserAPI(object):
    def __init__(self, api_key):
        super(ParserAPI, self).__init__()
        self.api_key = api_key
        self._session = requests.Session()

    def parse(self, url):
        url = '{0}{1}'.format(MERCURY_API, url)
        headers = {'x-api-key': self.api_key}

        r = self._session.get(url, headers=headers)
        p = ParsedArticle.from_dict(r.json(), parser=self)
        return p



