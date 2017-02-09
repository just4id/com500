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
    if len(para) < 2 and 1 < len(para):
        cmd.execute(['scrapy', 'crawl', para[1]])
    else:
        cmd.execute(['scrapy', 'crawl', 'ouzhi'])
