# 扫描北京的望京地区(d23008613-b18335711)租房情况,需要更改其它区域,只需要更改基本的url地址，可以通过自如的官网可查
# 生成的结果会存在当前目录下的result.csv文件里面
# 文件格式为: 时间, 房间名称, 房间空间大小(平方), 所在楼层, 所在楼房最高楼层, 房间详情链接
# 日志会在当前目录下的 ziroom_list.log

import re
import logging
import datetime
import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename='ziroom_list.log', level=logging.INFO)

PAGE_PATTERN = re.compile(r'\d')
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
           'Host': 'www.ziroom.com',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'}
# 房租最低价格
MIN_PRICE = 2500
# 房租最高价格
MAX_PRICE = 3000
# 房间最小面积
MIN_AREA = 12


def get_page(soup):
    hrefs = soup.find_all(id='page')[0]
    return int(PAGE_PATTERN.search(str(hrefs.span.string)).group())


def get_result(soup):
    items = soup.find(
        'div', class_='Z_list-box').find_all('div', class_='info-box')
    for item in items:
        area, focus = str(item.div.find('div', class_=False).string).replace(
            '㎡', '').strip('层').split('|')
        area, (focus1, focus2) = float(area.strip()), [
            int(r) for r in focus.strip().split('/')]
        # 超过7层一定是有电梯的
        if focus2 > 7:
            yield {'title': str(item.h5.string),
                   'area': area,
                   'high': focus1,
                   'max_high': focus2,
                   'url': item.h5.a['href'].strip('/')}


def get_soup(url):
    try:
        resp = requests.get(url, headers=HEADERS)
        assert resp.status_code == 200, 'error url'
    except Exception as e:
        logging.error(url)
        logging.error(e, exc_info=True)
    else:
        return BeautifulSoup(resp.content, 'html5lib')
    return ''


def filter_result(result):
    if result['area'] >= MIN_AREA:
        return result


def main():
    url = 'http://www.ziroom.com/z/d23008613-b18335711-r0-p{page}/?p=b2-n3&cp=%sTO%s&sort=5' % (MIN_PRICE, MAX_PRICE)
    init_page = get_soup(url.format(page=1))

    if not init_page:
        logging.info('init page error url: {}'.format(url.format(page=1)))
        return 1

    for page in range(1, get_page(init_page) + 1):
        soup = get_soup(url.format(page=page))
        for result in get_result(soup):
            if filter_result(result):
                yield result


if __name__ == "__main__":
    cnt = 0
    line_tpl = '{dt},{title},{area},{high},{max_high},{url}'
    dt = datetime.datetime.now().strftime('%F %H')
    with open('result.csv', 'a') as f:
        for result in main():
            result['dt'] = dt
            f.write('{}\n'.format(line_tpl.format(**result)))
            cnt += 1
    print('本次({})找到合适的租房数量: {}'.format(dt, cnt))
    logging.info('本次({})找到合适的租房数量: {}'.format(dt, cnt))
