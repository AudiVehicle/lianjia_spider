import requests
import parsel
import time
import csv
import datetime


def parse_one_page(url, region, csv_writer):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    selector = parsel.Selector(response.text)
    total = selector.css('.total span::text').get()
    iter = int(int(total) / 30)

    for page in range(1, iter):
        if page > 100:
            break
        print('===========================正在下载第{}页数据================================'.format(page))
        time.sleep(1)
        url = 'https://mianyang.lianjia.com/ershoufang/' + region + '/pg' + str(page) + '/'
        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)
        lis = selector.css('.sellListContent li')
        dit = {}
        for li in lis:
            title = li.css('.title a::text').get()
            dit['标题'] = title
            positionInfo = li.css('.positionInfo a::text').getall()
            info = '-'.join(positionInfo)
            dit['开发商'] = info
            houseInfo = li.css('.houseInfo::text').get()
            dit['房子信息'] = houseInfo
            followInfo = li.css('.followInfo::text').get()
            dit['发布周期'] = followInfo
            Price = li.css('.totalPrice span::text').get()
            dit['售价/万'] = Price
            unitPrice = li.css('.unitPrice span::text').get()
            dit['单价'] = unitPrice
            print(dit)
            csv_writer.writerow(dit)


def main(offset, csv_writer):
    regions = ['fuchengqu', 'youxianqu', 'anzhouqu', 'jiangyoushi', 'santaixian']
    for region in regions:
        for i in range(1, offset):
            url = 'https://mianyang.lianjia.com/ershoufang/' + region + '/pg' + str(i) + '/'
            parse_one_page(url, region, csv_writer)
            time.sleep(1)
        print('{} has been writen.'.format(region))


file_name = './data/绵阳二手房信息_' + str(datetime.date.today()) + '.csv'
f = open(file_name, mode='a', encoding='utf-8-sig', newline='')
csv_writer = csv.DictWriter(f, fieldnames=['标题', '开发商', '房子信息', '发布周期', '售价/万', '单价'])
csv_writer.writeheader()

main(2, csv_writer)
