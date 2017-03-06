# -*- coding: utf-8 -*-
'''
Created on 2016/07/25
@author: zhamingg
'''

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class YazhiSpider(Spider):
    name = "yazhi"
    allowed_domains = ["500.com"]
    fid = '397941'
    file_path = '.'
    sort_dict_europe = {}
    j = i = 0
    sleep_second = 0
    blank_d = 32

    xhr_url = "http://odds.500.com/fenxi1/inc/yazhiajax.php?fid=%s&id=%s&r=1&t=1469551520048"
    start_urls = ["http://odds.500.com/fenxi/yazhi-%s.shtml" %fid]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://odds.500.com/fenxi/ouzhi-397941.shtml
        @scrapes name
        """
        sel = Selector(response)
        trs = sel.xpath('//div[@class="odds_content odds_yazhi"]/div[@id="table_cont"]/table[@id="datatb"]/tr[@xls="row"]')
        row_no = 0

        for tr in trs:
            att = tr.root.attrib
            id = att.get('id')
            dt = att.get('dt')
            row_no += 1
            url = ''
            title = ''
            onclick = ''

            td_index = 0
            tds = tr.xpath('td')
            for td in tds:
                if td_index > 2:
                    break
                elif td_index == 0:
                    td_index += 1
                    continue
                elif td_index == 1:
                    td_att = td.root.attrib
                    title = td_att.get('title')
                    a_href = td.xpath('p/a/@href')
                    url = a_href.extract()
                elif td_index == 2:
                    onclick_tds = td.xpath('table/tbody/tr/td')
                    
                    for on_c in onclick_tds:
                        onclick = on_c.root.attrib.get('onclick')
                        break

                td_index += 1

            item = dict()
            item['row_no'] = row_no
            item['title'] = title
            item['id'] = id
            item['dt'] = dt
            item['url'] = url
            item['onclick'] = onclick
            
            x_url_u = self.xhr_url %(self.fid, id)
            self.sort_dict_europe[x_url_u] = [row_no, item]

        for x_url in self.sort_dict_europe.keys():
            time.sleep(self.sleep_second)
            req = Request(x_url,
                              callback=self.parse_code,
                              meta={'item': item})
            yield req

    def parse_code(self, response):
        x_url = response.url.replace('%20', ' ')
        row_no = str(self.sort_dict_europe[x_url][0])
        com_name = self.sort_dict_europe[x_url][1].get('title')
        header = '%s%s(%s)' %('No.', row_no, str(com_name))
        header = (header + (' ' * (self.blank_d - len(header)))) if len(header) < self.blank_d else header
        line = '%s:%s' %(header, response.body)
        
        self.gen_file(line, self.name)
        return {row_no: line}
    
    def gen_file(self, line, d_type):
        filename = os.path.join(self.file_path, ('com500-%s.txt' % d_type))

        f = None
        try:
            f = open(filename, ("%s" %('w' if self.i == 0 else 'a')))
            self.i += 1
            # print line
            f.write(str(line) + '\n')
        except Exception, e:
            print e
        finally:
            if f:
                f.close()
