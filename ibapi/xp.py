import os
import time
import logging
import requests
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree


default_headers = {
    'Accept-Language': 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
    'Connection': 'keep-alive',
    'Host': 'portal.xpi.com.br',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
}


logger = logging.getLogger('ibapi')

class Session(object):
    def __init__(self, account, passwd=None, passwd_cb=None, url=None):
        '''
        account: the XP login number
        pwmethod: the authentication method (either 'plain', or 'shuffle')

        When authenticating on XP website, one has to press the button
        containing the digits of its password in the correct order. There are a
        total of 5 buttons containing 3 digits each.
        '''
        self.account = account
        self.driver = None
        self.passwd = passwd
        self.passwd_cb = passwd_cb
        self.url = url or 'https://portal.xpi.com.br'

    def __enter__(self):
        return self

    def start(self):
        logger.info('starting XP session for account {}'.format(self.account))
        self.driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        logger.info('navigating to {}'.format(self.url))
        self.driver.get(self.url)
        el = self.get('txtLogin')
        el.clear()
        el.send_keys(self.account)
        el = self.get('btnOkLogin')
        el.click()
        el = self.get('lnkNomeUsuario', timeout=120)
        el.click()
        logger.info('feeding password')
        ids = ['btnPass0', 'btnPass1', 'btnPass2', 'btnPass3', 'btnPass4']
        btns = [self.get(id) for id in ids]
        numbers = self._parse_numbers([b.text for b in btns])
        logger.info('XP password buttons are {}'.format(' '.join(numbers)))
        if self.passwd_cb:
            order = self.passwd_cb(numbers)
        else:
            order = []
            for x in self.passwd:
                for i, num in enumerate(numbers):
                    if x in num:
                        order.append(i)
                        break
        for i in order:
            btns[i].click()
            time.sleep(0.5)
        el = self.get('btnEntrar')
        el.click()
        el = self.get('cphMinhaConta_wcDefault1_wcLateralInfo1_lblNomeCliente')
        logger.info('logging successful, welcome {}'.format(el.text))

    def list_notas(self):
        headers = default_headers.copy()
        headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Referer': 'https://portal.xpi.com.br/acoes-opcoes-futuros/posicao-geral',
            'Upgrade-Insecure-Requests': '1',
        })
        cookies = self.get_cookies()
        url = 'https://portal.xpi.com.br/acoes-opcoes-futuros/notas-corretagem'
        req = requests.get(url, cookies=cookies, headers=headers)
        parser = etree.HTMLParser()
        tree = etree.fromstring(req.text, parser)
        return [date(*map(int, reversed(x.split('/'))))
                for x in tree.xpath('//*[@id="Data"]/option/text()')]

    def get_nota(self, date):
        date_str = date.strftime('%d/%m/%Y')
        headers = default_headers.copy()
        headers.update({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Length': '51',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://portal.xpi.com.br',
            'Referer': 'https://portal.xpi.com.br/acoes-opcoes-futuros/notas-corretagem',
            'X-Requested-With': 'XMLHttpRequest',
        })
        data = {
            'Data': date_str,
            'X-Requested-With': 'XMLHttpRequest',
        }
        xpnotaurl = 'https://portal.xpi.com.br/acoes-opcoes-futuros/NotasCorretagem/ExibirExtrato'
        cookies = self.get_cookies()
        req = requests.post(xpnotaurl,
                            data=data,
                            cookies=cookies,
                            headers=headers)
        return req.json()

    def get_cookies(self):
        return {c['name']: c['value'] for c in self.driver.get_cookies()}

    def __exit__(self, e_typ, e_val, trcbak):
        if self.driver:
            self.driver.close()

    def _parse_numbers(self, txts):
        return [''.join(txt.split(' ou ')) for txt in txts]

    def get(self, id, timeout=60, by=By.ID):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, id)))
