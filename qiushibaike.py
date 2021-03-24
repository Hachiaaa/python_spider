import requests
from requests.exceptions import RequestException
import time
import re
from bs4 import BeautifulSoup
from functools import reduce

url = 'https://www.qiushibaike.com/text/page/{}/'

MAX_SIZE = 13

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Referer': 'https://www.qiushibaike.com'
}

cookies_str = '''_xsrf=2|0e13af70|073114e08f9147c1d443405e2a7c0fe1|1604497589;gr_user_id=811b9b3e-58c1-4ff7-b284-f9dc13c955d4; grwng_uid=12503176-371a-4ecd-8e88-9e17c37f9070; _ga=GA1.2.757605610.1604497588; _gid=GA1.2.1746
274786.1604497588; __cur_art_index=7600; ff2672c245bd193c6261e9ab2cd35865_gr_session_id=4ed01c20-d13e-4d26-bc4
e-8b1f3df7abb8; ff2672c245bd193c6261e9ab2cd35865_gr_session_id_4ed01c20-d13e-4d26-bc4e-8b1f3df7abb8=true; _gat=1; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1604581011'''

f = open('qiushi.txt', 'w+', encoding='utf-8')

cookies = {}

for item in cookies_str.split(';'):
    name, value = item.strip().split('=', 1)
    cookies[name] = value



def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if (response.status_code == 200):
            return response.text
    except RequestException:
        print('there is something wrong!')
        return None


def parse_list_content(html_content):
    parsed_res = []
    soup = BeautifulSoup(html_content, 'lxml')
    all_content = soup('div', id=re.compile('qiushi_tag'))
    for item in all_content:
        parsed_res.append({
            'author':
            item('h2')[0].string.strip(),
            'href':
            'https://www.qiushibaike.com' +
            item('a', class_='contentHerf')[0].attrs['href']
        })
    return parsed_res


def parse_article_content(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    return soup('div', class_='content')[0].stripped_strings


def main():
    for i in range(1, MAX_SIZE + 1):
        html_content = get_one_page(url.format(i))
        parsed_res = parse_list_content(html_content)
        for item in parsed_res:
            html_text = get_one_page(item['href'])
            content = parse_article_content(html_text)
            print(item)
            f.write(item['author'])
            f.write('\n')
            f.write('')
            f.write(reduce(lambda x, y: x + y, list(content)))
            f.write('\n')
            f.write('------------------------------------------')
            f.write('\n')
    f.close()
    print('done')


if __name__ == '__main__':
    print(cookies)
    main()
