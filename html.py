# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 20:56:43 2015

@author: Gábor
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas.io.html import read_html


class Ticker:
    
    def __init__(self, ticker, date=None):
        self.ticker = ticker
        self.YAHOO_ENDPOINT = 'http://finance.yahoo.com/q/'
        self.PAGE_URLS = {
            'major_holders':        '{}mh'.format(self.YAHOO_ENDPOINT),
            'insider_transactions': '{}it'.format(self.YAHOO_ENDPOINT),
            'key_statistics':       '{}ks'.format(self.YAHOO_ENDPOINT),
            'headline':             '{}h'.format(self.YAHOO_ENDPOINT),
            'competitors':          '{}co'.format(self.YAHOO_ENDPOINT),
            'competitors':          '{}co'.format(self.YAHOO_ENDPOINT),
        }
        self.params = {'s':ticker}
        if date:
            self.params['t'] = date
    
    def get(self, page_type):
        assert page_type in self.PAGE_URLS.keys()
        url = self.PAGE_URLS[page_type]
        resp = requests.get(url, params=self.params)
        if resp.status_code != 200:
            self.text = ''            
        self.text = resp.text
        self.page_type = page_type
        return self
    
    def parse(self, table):
        q = BeautifulSoup(self.text)
        if table == 'breakdown':
            self.table = q.findAll(attrs={"id": "yfi_holders_breakdown"})[0]
        if table == 'persons':
            self.table = q.findAll(attrs={"class": "yfnc_tableout1"})[0]
        if table == 'institutions':
            self.table = q.findAll(attrs={"class": "yfnc_tableout1"})[1]
        if table == 'funds':
            self.table = q.findAll(attrs={"class": "yfnc_tableout1"})[2]     
        return self

    def as_df(self, header=True):
        self.df = read_html(unicode(self.table), header=header)
        return self
        
        
ticker = Ticker('AAPL')
ticker.get('major_holders')
ticker.parse('funds')
ticker.as_df(header=False)
ticker.df[2]
            .parse('breakdown') \
            .parse('institutions') \
            .parse('funds')



a = Html('AAPL').get('insider_transactions')
a = Html('AAPL').get('key_statistics')
a = Html('AAPL', date='2015-02-16').get('headline')
