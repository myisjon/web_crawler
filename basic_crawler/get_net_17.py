"""
    获取 17K 免费读书章节
"""

import requests
from bs4 import BeautifulSoup

def do_request(url, headers=None):
    if headers is None:
        req = requests.get(url)
    else:
        req = requests.get(url, headers=headers)

    if req.status_code not in [200, ]:
        with open('error_url.log', 'a') as f:
            f.write(url)
            return ''
    return req.content


def do_soup(content):
    soup = BeautifulSoup(content, 'html.parser')
    soup = soup.find('div', id='readArea')
    soup = soup.find('div', class_='readAreaBox content')
    h1 = '{}\n'.format(soup.h1.string)
    soup = soup.find('div', class_='p')
    texts = [h1,]
    for text in soup.contents:
        if text.string:
            texts.append(text.string.strip())

    text = '\n'.join(texts)
    with open('shendi.txt', 'a') as f:
        f.write('{}\n'.format(text))

def get_url(content):
    soup = BeautifulSoup(content, 'html.parser')
    soup = soup.find('dl', class_='Volume')
    links = soup.dd.find_all('a', target='_blank')
    for link in links:
        yield link['href']

def main():
    host = 'http://www.17k.com'
    main_uri = '/list/2744031.html'

    for uri in get_url(do_request('{}{}'.format(host, main_uri))):
        print(uri)
        do_soup(do_request('{}{}'.format(host, uri)))

if __name__ == '__main__' :
    main()