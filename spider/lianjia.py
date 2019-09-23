#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zhiqi.chen
# @Date: 2019-08-20 14:22:24
# @Software: Visual Studio Code
import requests
from pyquery import PyQuery as pq
import csv
import sys
import json
import datetime

class LianJiaZuFang():
    def __init__(self):
        self.city = 'cd'
        self.district = 'shuangliu'
        self.hourse_info = []
    
    def get_index(self, url):
        try:
            response = requests.get(url)
            # 当进入没有租房信息的页面时，将已爬取的数据存入csv并退出程序
            if "没有找到" in response.text:
                print('No more hourse!')
                self.save_csv()
                sys.exit()
            elif response.status_code == 200:
                print('Get url:', url)
                return response.text
            return None
        except ConnectionError:
            return None
    
    def parse_index(self, html):
        doc = pq(html)
        hourse_list = doc('.house-lst li').items()
        for hourse in hourse_list:
            title = hourse('.info-panel h2').text().replace(" ", "-").replace("，", "-")
            desc_initial = hourse('.where').text().split()
            desc = "-".join(desc_initial)  # 格式处理
            tags = hourse('.con').text()
            location = '成都' + desc_initial[0]
            price = hourse('.price span').text()
            update_time = hourse('.price-pre').text()[0:-3]
            hourse_url = hourse('.pic-panel a').attr('href')
            img_url = hourse('.pic-panel img').attr('data-img')
        
            self.hourse_info.append([title, desc, tags, location, longitude, latitude, price, update_time, hourse_url, img_url])
            self.hourse_dict = {
                'title': title,
                'desc': desc,
                'tags': tags,
                'location': location,
                'longitude': longitude,
                'latitude': latitude,
                'price': price,
                'update_time': update_time,
                'hourse_url': hourse_url,
                'img_url': img_url,
                }
                
            self.save_csv()
    def save_csv(self):
        with open('zufang-{}.csv'.format(self.city), 'w', encoding='utf8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['租房标题', '描述', '标签', '位置', '经度', '纬度', '价格/月', '更新日期', '房屋详情页', '图片url'])
            for row in self.hourse_info:
                writer.writerow(row)
    
    def main(self):
        start_time = datetime.datetime.now()
        for page in range(1,101):
            # 爬取xx市的url
            # url = 'https://{0}.lianjia.com/zufang/pg{1}'.format(self.city, page)
            # 爬取xx市xx区的url
            url = 'https://{0}.lianjia.com/zufang/{1}/pg{2}'.format(self.city, self.district, page)
            html = self.get_index(url)
            self.parse_index(html)
            crawl_time = datetime.datetime.now() - start_time
            print(crawl_time)

if __name__ == "__main__":
    zf = LianJiaZuFang()
    zf.main()
