import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

URL = 'http://www.86pm25.com/paiming.htm'


class AirIndex:
    def __init__(self, url):
        self.url = url
        self.rank = {}
        self.shenghui_list = [
            '北京', '上海', '天津', '重庆', '哈尔滨', '长春', '沈阳', '呼和浩特', '石家庄', '乌鲁木齐',
            '兰州', '西宁', '西安', '银川', '郑州', '济南', '太原', '合肥', '武汉', '长沙', '南京',
            '成都', '贵阳', '昆明', '南宁', '拉萨', '杭州', '南昌', '广州', '福州', '台北', '海口',
            '香港', '澳门'
        ]
        self.shenghuirank = {}

    def get_sort_content(self):
        try:
            res = requests.get(self.url, headers=HEADERS, timeout=3)
            if (res.status_code == 200):
                res.encoding = 'utf-8'
                self.content = res.text
        except RequestException:
            print('there is something wrong about request')

    def parse_content(self):
        soup = BeautifulSoup(self.content, 'lxml')
        all_city = soup.find('table', id='goodtable').find_all('tr')
        for item in list(all_city)[1:]:
            single_data = list(item.find_all('td'))
            city = single_data[1].string
            rank = single_data[0].string.strip()
            if city.replace('市', "") in self.shenghui_list:
                self.shenghuirank[city] = rank
            self.rank[city] = rank
        print(self.shenghuirank)


def main():
    spider = AirIndex(URL)
    spider.get_sort_content()
    spider.parse_content()


if __name__ == '__main__':
    main()
