import unittest
from alinkcheck.findurls import GetUrls

class TestEmpty(unittest.TestCase):
    def test_no_urls(self):
        fname = 'no_links.txt'
        g = GetUrls(fname, None)
        self.assertEqual(g.urls, [])

class TestTXT(unittest.TestCase):
    def test_parse_text(self):
        fname = 'retest.txt'
        g = GetUrls(fname, None)
        url_list = [['http://en.wikipedia.org/wiki/Body_image', 'http://en.wikipedia.org/wiki/Identity_formation',
            'http://en.wikipedia.org/wiki/Self-confidence', 'http://en.wikipedia.org/wiki/Self-esteem'],
            ['http://www.bbc.com/sport/0/'], ['http://www.haskell.org/'], ['http://lxer.com/'],
            ['http://www.find-happiness.com/definition-of-happiness.html'],
            ['http://www.wikihow.com/Elevate-Your-Self-Esteem']]
        self.assertCountEqual(g.urls, url_list)

class TestJSON(unittest.TestCase):
    def test_parse_json_list(self):
        fname = 'url_list.json'
        g = GetUrls(fname, None)
        url_list = [['http://en.wikipedia.org/wiki/Body_image', 'http://en.wikipedia.org/wiki/Identity_formation',
                'http://en.wikipedia.org/wiki/Self-confidence', 'http://en.wikipedia.org/wiki/Self-esteem',
                'http://en.wikipedia.org/wiki/Shyness', 'http://en.wikipedia.org/wiki/Anger', 'http://en.wikipedia.org/wiki/Anxiety',
                'http://en.wikipedia.org/wiki/Fear'], ['http://www.wikihow.com/Elevate-Your-Self-Esteem',
                'http://www.wikihow.com/Get-Rid-of-Anger']]
        self.assertCountEqual(g.urls, url_list)

    def test_keyname(self):
        fname = 'keyname_test.json'
        g = GetUrls(fname, 'resource_url')
        url_list = [['http://www.python.org/'], ['http://www.elixir-lang.org/'], ['http://www.haskell.org/']]
        self.assertCountEqual(g.urls, url_list)

    def test_wrong_keyname(self):
        fname = 'keyname_test.json'
        g = GetUrls(fname, 'source_url')
        url_list = [['http://www.python.org/'], ['http://www.elixir-lang.org/'], ['http://www.haskell.org/']]
        self.assertCountEqual(g.urls, url_list)

if __name__ == '__main__':
    unittest.main()
