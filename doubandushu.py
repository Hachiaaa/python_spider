import requests
from requests.exceptions import RequestException
import re
import time
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

url = 'https://book.douban.com/top250?start={}'
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def get_one_page(index):
    try:
        response = requests.get(url.format(index * 25), headers=headers)
        if (response.status_code == 200):
            return response.text
    except RequestException:
        print('there is something wrong!')
        return None


def parse_content_by_re(html_content):
    re_obj = re.compile(
        '<div class="pl2">.*?>(.*?)</a>.*?<p class="pl">(.*?)</p>.*?<span class="rating_nums">(.*?)</span>.*?<span class="pl">\((.*?)\)</span>',
        re.S)
    parsed_res = re.findall(re_obj, html_content)
    for item in parsed_res:
        sub_title_res = re.findall('<span.*?>(.*?)</span>', item[0])
        sub_title = sub_title_res[0] if len(sub_title_res) > 0 else ''
        yield {
            'title':
            re.sub('<span.*?</span>', '', item[0]).strip() + sub_title.strip(),
            'author':
            item[1][0:item[1].index('/')].strip(),
            'rating_score':
            item[2].strip(),
            'rating_nums':
            item[3].strip()[0:-3],
            # 'short_intro':item[4].strip()
        }


def parse_content_by_bs4(html_content):
    bs4_obj = BeautifulSoup(html_content, 'lxml')
    for i in range(1, 26):
        title = bs4_obj.select(
            "#content > div > div.article > div > table:nth-of-type({}) > tbody > tr > td:nth-child(2) > div.pl2 > a"
            .format(i))
        sub_title = bs4_obj.select(
            "#content > div > div.article > div > table:nth-of-type({}) > tbody > tr > td:nth-child(2) > div.pl2 > a > span"
            .format(i))[0].string
        author = bs4_obj.select(
            "#content > div > div.article > div > table:nth-of-type({}) > tbody > tr > td:nth-child(2) > p.pl"
            .format(i))[0].string
        rating_score = bs4_obj.select(
            "#content > div > div.article > div > table:nth-of-type({}) > tbody > tr > td:nth-child(2) > div.star.clearfix > span.rating_nums"
            .format(i))[0].string
        rating_nums = bs4_obj.select(
            "#content > div > div.article > div > table:nth-of-type({}) > tbody > tr > td:nth-child(2) > div.star.clearfix > span.pl"
            .format(i))[0].string
        short_intro = bs4_obj.select(
            "#content > div > div.article > div > table:nth-of-type({}) > tbody > tr > td:nth-child(2) > p.quote > span"
            .format(i))[0].string
        yield {title, sub_title, author, rating_score, rating_nums, short_nums}


def parse_content_by_pq(html_content):
    pq_obj = pq(html_content)
    for i in range(1, 26):
        title = pq_obj(
            "#content > div > div.article > div > table:nth-of-type({})   tr > td:nth-child(2) > div.pl2 > a"
            .format(i)).text()
        author = pq_obj(
            "#content > div > div.article > div > table:nth-of-type({})   tr > td:nth-child(2) > p.pl"
            .format(i)).text()
        rating_score = pq_obj(
            "#content > div > div.article > div > table:nth-of-type({})   tr > td:nth-child(2) > div.star.clearfix > span.rating_nums"
            .format(i)).text()
        rating_nums = pq_obj(
            "#content > div > div.article > div > table:nth-of-type({})   tr > td:nth-child(2) > div.star.clearfix > span.pl"
            .format(i)).text()
        short_intro = pq_obj(
            "#content > div > div.article > div > table:nth-of-type({})  tr > td:nth-child(2) > p.quote > span"
            .format(i)).text()
        yield {
            'title': title,
            'author': author,
            'rating_score': rating_score,
            'rating_nums': rating_nums,
            'short_intro': short_intro
        }


def main():
    global a
    for i in range(10):
        time.sleep(1)
        html_text = get_one_page(i)
        parsed_res = parse_content_by_pq(html_text)
        for item in parsed_res:
            print(item)


if __name__ == '__main__':
    main()
