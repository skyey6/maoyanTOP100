import requests
import re
import json
import time


def get_one_page(url):
    """
    获得猫眼TOP100网页源码
    :param url:网站的url
    :return:能够获取则返回网页源码，否则返回None
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Cookie': '__mta=45995675.1610887137467.1611039201655.1611039405118.10; uuid_n_v=v1; uuid=F5FB14D058C011EB9D2469655334980CA1B86370E3D947679318FC849C8931E3; _csrf=f767f33be1890a9b5ccd52f5f37de829fb08bb88e33a0519ea42a006c0f2ff3b; _lxsdk_cuid=177105b085ac8-0e74e6d70d4d74-c791039-1fa400-177105b085ac8; _lxsdk=F5FB14D058C011EB9D2469655334980CA1B86370E3D947679318FC849C8931E3; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1610887137,1611029607,1611039389; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=45995675.1610887137467.1611039201655.1611039401819.10; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1611039405; _lxsdk_s=177194fdd92-e55-dbb-eb0%7C%7C20'
        # Cookie如果失效可自行更改
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_one_page(html):
    """
    对获得的网页源码进行处理，获取需要的信息
    :param html:需要处理的html代码
    """
    pattern = re.compile(
        r'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>上映时间：(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actors': item[3].strip(),
            'releasetime': item[4],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    with open('maoyanTop100.txt', 'a', encoding='utf-8') as f:
        # 通过json.dumps()将字典变成json字符串
        # ensure_ascii参数设置为False保证输出结果是中文而不是Unicode编码
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    for x in range(10):
        maoyan = f'https://maoyan.com/board/4?offset={x*10}'
        text = get_one_page(maoyan)
        result = parse_one_page(text)
        for i in result:
            write_to_file(i)
        time.sleep(0.5)   # 减慢爬取速度，防反爬虫机制
    print('爬取完毕')
