'''
Created on 2016/07/23
@author: zhamingg
'''
import scrapy.cmdline as cmd
import sys 

if __name__ == "__main__":
    '''
    usage: python run_scrapy.py [ouzhi | yazhi]
    '''
    para = sys.argv
    if len(para) == 2:
        fid = para[1]
        cmd.execute(['scrapy', 'crawl', 'ouzhi', '-a fid=%s' %fid])