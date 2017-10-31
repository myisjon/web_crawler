import requests
from bs4 import BeautifulSoup


def do_request(url, headers=None):
    if headers is None:
        req = requests.get(url)
    else:
        req = requests.get(url, headers=headers)

    if req.status_code > 300:
        with open('error_url.log', 'a') as f:
            f.write('{}\t{}'.format(req.status_code, url))
        return False

    return req.content


def do_soup(content):
    soups = BeautifulSoup(content, 'html.parser')
    soups = soups.find(id='div_main_content')
    next_uri = soups.find(class_="pgs cl mtm")
    next_uri = next_uri.find(class_='nxt')
    if next_uri is not None:
        next_uri = next_uri['href']
    soups = soups.find(id="comment_ul")
    comments = []
    for comment in soups.findAll("dl"):
        comments.append(
            comment.text.strip(
            ).replace('\xa0\xa0', ':').replace('\n\n\n\n\n\n', '\n').replace('\r\n', '\n').replace('\n\n\n', '\n'))

    return (next_uri, comments)


def main():
    uri = 'http://bbs.sciencenet.cn/home.php?mod=space&uid=496649&do=wall'
    with open('bbs.sciencenet.cn_496649.txt', 'a') as f:
        while uri is not None:
            print('collect uri: ', uri)
            (uri, comments) = do_soup(do_request(uri))
            separator = '\n{}\n'.format('=' * 10)
            f.write(separator.join(comments))
        print('collect is ok')


if __name__ == '__main__':
    main()
