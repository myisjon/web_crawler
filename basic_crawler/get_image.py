import os
import time
import json
import requests


IMAG_URL = 'http://cn.bing.com{path}'
IMG_API_URL = 'http://cn.bing.com/HPImageArchive.aspx'
PARAMS = {
    'format': 'js',
    'idx': 0,
    'n': 1,
    'nc': int(time.time() * 1000),
    'pid': 'hp',
    'mkt': 'zh-CN',
}


def get_img_url(img_api_url, params):
    req = requests.get(img_api_url, params=params)
    json_text = ''
    if req.status_code in [200, ]:
        json_text = json.loads(req.text)

    if not json_text:
        return ''
    return IMAG_URL.format(path=json_text['images'][0]['url'])


def get_img(img_url):
    req = requests.get(img_url, stream=True)
    postfix = img_url[img_url.rfind('.'):]
    img_path = '{}{}'.format(time.strftime("%Y_%m_%d", time.localtime()), postfix)
    with open(img_path, 'wb') as f:
        for img_stream in req.iter_content(chunk_size=1024):
            f.write(img_stream)
            f.flush()

    return os.path.abspath(img_path)


def main():
    img_path = get_img(get_img_url(IMG_API_URL, PARAMS))
    print(img_path)


if __name__ == '__main__':
    main()
