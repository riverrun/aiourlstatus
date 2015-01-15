import unittest
from aiourlstatus import app

class TestEmpty(unittest.TestCase):
    def test_no_urls(self):
        data = ''
        urls, len_urls = app.find_sort_urls(data)
        self.assertEqual(urls, [])
        self.assertEqual(len_urls, 0)

class TestTXT(unittest.TestCase):
    def test_parse_text(self):
        with open('tests/retest.txt') as f:
            data = f.read()
        urls, len_urls = app.find_sort_urls(data)
        url_list = [['http://en.wikipedia.org/wiki/Body_image', 'http://en.wikipedia.org/wiki/Identity_formation',
            'http://en.wikipedia.org/wiki/Self-confidence', 'http://en.wikipedia.org/wiki/Self-esteem'],
            ['http://www.bbc.com/sport/0/'], ['http://www.haskell.org/'], ['http://lxer.com/'],
            ['http://www.find-happiness.com/definition-of-happiness.html'],
            ['http://www.wikihow.com/Elevate-Your-Self-Esteem']]
        self.assertCountEqual(urls, url_list)

if __name__ == '__main__':
    unittest.main()
