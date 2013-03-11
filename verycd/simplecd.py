
from urllib.request import urlopen
import re


def simplecd_links(url):
    m = re.match(r'(http://(?:www\.)?s[ia]mplecd\.\w+/)(id|entry)/', url)
    assert m, url
    site = m.group(1)
    html = urlopen(url).read().decode('utf-8')
    ids = re.findall(r'value="(\w+)"\s+name="selectemule"', html)
    form = '&'.join('rid=' + id for id in ids)
    q = 'mode=copy&' + form
    html = urlopen(site + 'download/?' + q).read().decode('utf-8')
    table = re.search(r'<table id="showall" .*?</table>', html, flags=re.S).group()
    links = re.findall(r'ed2k://[^\s<>]+', table)
    return links


def extend_link(url):
    links = simplecd_links(url)
    from myLib import parse_ed2k_file
    return [{'url':x, 'name':parse_ed2k_file(x)} for x in links]


def test():
    url = 'http://simplecd.me/entry/gAwlxX80/'
    items = extend_link(url)
    for item in items:
        print(item['name'], item['url'])


if __name__ == '__main__':
    test()