import unittest
from alinkcheck.app import GetUrls

class TestEmpty(unittest.TestCase):
    def test_no_urls(self):
        fname = 'no_links.txt'
        g = GetUrls(fname)
        self.assertEqual(g.urls, [])

class TestTXT(unittest.TestCase):
    def test_parse_text(self):
        fname = 'retest.txt'
        g = GetUrls(fname)
        url_list = ['http://www.bbc.com/sport/0/', 'http://www.haskell.org/', 'http://lxer.com/',
                'http://en.wikipedia.org/wiki/Body_image', 'http://www.find-happiness.com/definition-of-happiness.html',
                'http://en.wikipedia.org/wiki/Identity_formation', 'http://en.wikipedia.org/wiki/Self-confidence',
                'http://en.wikipedia.org/wiki/Self-esteem', 'http://www.wikihow.com/Elevate-Your-Self-Esteem']
        self.assertEqual(g.urls, url_list)

class TestJSON(unittest.TestCase):
    def test_parse_json_list(self):
        fname = 'url_list.json'
        g = GetUrls(fname)
        url_list = ['http://en.wikipedia.org/wiki/Body_image', 'http://en.wikipedia.org/wiki/Identity_formation',
                'http://en.wikipedia.org/wiki/Self-confidence', 'http://en.wikipedia.org/wiki/Self-esteem',
                'http://www.wikihow.com/Elevate-Your-Self-Esteem', 'http://en.wikipedia.org/wiki/Shyness',
                'http://en.wikipedia.org/wiki/Anger', 'http://www.wikihow.com/Get-Rid-of-Anger',
                'http://www.wikihow.com/Get-Rid-of-Anger', 'http://en.wikipedia.org/wiki/Anxiety', 'http://en.wikipedia.org/wiki/Fear']
        self.assertEqual(g.urls, url_list)

if __name__ == '__main__':
    unittest.main()
