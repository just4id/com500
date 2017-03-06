# -*- coding: utf-8 -*-
'''
Created on 2016/07/23
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

class DmozSpider(Spider):
    name = "ouzhi"
    
    def __init__(self, **kwargs):
        self.fid = kwargs.values()[0]
        self.start_urls = ["http://odds.500.com/fenxi/ouzhi-%s.shtml" %self.fid]
        print self.start_urls 
        super(DmozSpider, self).__init__(**kwargs)

    fid = 596481
    allowed_domains = ["500.com"]
    types = ['europe', 'kelly']
    file_path = '.'
    sort_dict_europe = sort_dict_kelly = {}
    j = i = 0
    sleep_second = 0
    blank_d = 32

    xhr_url = "http://odds.500.com/fenxi1/json/ouzhi.php?fid=%s&cid=%s&r=1&time=%s&type=%s"
    start_urls = None

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://odds.500.com/fenxi/ouzhi-397941.shtml
        @scrapes name
        """
        sel = Selector(response)
        trs = sel.xpath('//div[@class="odds_content"]/div[@id="table_cont"]/table[@id="datatb"]/tr[@xls="row"]')
        row_no = 0

        for tr in trs:
            att = tr.root.attrib
            cid = att.get('id')
            data_time = att.get('data-time')
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
            item['cid'] = cid
            item['data_time'] = data_time
            item['url'] = url
            item['onclick'] = onclick
            
            x_url_u = self.xhr_url %(self.fid, cid, data_time, self.types[0])
            self.sort_dict_europe[x_url_u] = [row_no, item]
#             x_url_k = self.xhr_url %(self.fid, cid, data_time, self.types[1])
#             self.sort_dict_kelly[x_url_k] = [row_no, item]
        
        for x_url in self.sort_dict_europe.keys():
            time.sleep(self.sleep_second)
            req = Request(x_url,
                              callback=self.parse_code,
                              meta={'item': item})
            yield req

        '''
        for x_url in self.sort_dict_kelly.keys():
            time.sleep(self.sleep_second)
            req = Request(x_url,
                              callback=self.parse_code,
                              meta={'item': item})
            yield req
        '''
    def parse_code(self, response):
        x_url = response.url.replace('%20', ' ')
        d_type = self.types[0] if self.types[0] in x_url else self.types[1]
        row_no = str(self.sort_dict_europe[x_url][0] if self.types[0] in x_url  else self.sort_dict_kelly[x_url][0])
        com_name = self.sort_dict_europe[x_url][1].get('title')
        header = '%s%s(%s)' %('No.', row_no, str(com_name))
        header = (header + (' ' * (self.blank_d - len(header)))) if len(header) < self.blank_d else header
        line = '%s:%s' %(header, response.body)
        
        self.gen_file(line, d_type)

        return {row_no: line}
    
    def gen_file(self, line, d_type):
        filename = os.path.join(self.file_path, ('com500-%s-%s-%s.txt' %(self.fid, self.name, d_type)))

        f = None
        try:
            if self.types[0] in d_type:
                f = open(filename,("%s" %('w' if self.i == 0 else 'a'))) 
                self.i += 1
            else:
                f = open(filename,("%s" %('w' if self.j == 0 else 'a')))
                self.j += 1
            # print line
            f.write(str(line) + '\n')
        except Exception, e:
            print e
        finally:
            if f:
                f.close()
