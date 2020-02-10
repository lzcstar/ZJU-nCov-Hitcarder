# -*- coding: utf-8 -*-
import requests, json, re
import time, datetime, os
import getpass
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from halo import Halo
from apscheduler.schedulers.blocking import BlockingScheduler

class DaKa(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # self.driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
        self.driver = webdriver.PhantomJS('./phantomjs')
        self.base_url = "https://healthreport.zju.edu.cn/ncov/wap/default/index"
        self.save_url = "https://healthreport.zju.edu.cn/ncov/wap/default/save"
        self.sess = requests.Session()
    
    def login(self):
        driver = self.driver
        driver.get("https://zjuam.zju.edu.cn/cas/login?service=https%3A%2F%2Fhealthreport.zju.edu.cn%2Fa_zju%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fhealthreport.zju.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex")
        driver.find_element_by_id("username").send_keys(self.username)
        driver.find_element_by_id("password").send_keys(self.password)
        driver.find_element_by_id("dl").click()
        self.cookies = driver.get_cookies()
        cookie = [item["name"] + "=" + item["value"] for item in self.cookies ]
        self.cookiestr = '; '.join(item for item in cookie)
        driver.close()
        return self.cookiestr
    
    def post(self):
        self.update_sess()
        res = self.sess.post(self.save_url, data=self.info)
        return json.loads(res.text)
    
    def update_sess(self):
        self.sess.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Cookie': self.cookiestr,
        })
    
    def get_date(self):
        today = datetime.date.today()
        return "%4d%02d%02d" %(today.year, today.month, today.day)
        
    def get_info(self, html=None):
        if not html:
            self.update_sess()
            res = self.sess.get(self.base_url)
            html = res.content.decode()
        
        old_info = json.loads(re.findall(r'oldInfo: ({[^}]+})', html)[0])
        name = re.findall(r'realname: "([^\"]+)",', html)[0]
        number = re.findall(r"number: '([^\']+)',", html)[0]

        new_info = old_info.copy()
        new_info['name'] = name
        new_info['number'] = number
        new_info["date"] = self.get_date()
        new_info["created"] = round(time.time())
        self.info = new_info
        return new_info


def main(username, password):
    print("\n🚌 打卡任务启动")
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start('启动phantomJS浏览器...')
    dk = DaKa(username, password)
    spinner.succeed('已启动phantomJS浏览器')

    spinner.start(text='登录到浙大统一身份认证平台...')
    dk.login()
    spinner.succeed('已登录到浙大统一身份认证平台')

    spinner.start(text='正在获取个人信息...')
    dk.get_info()
    spinner.succeed('%s %s同学, 你好~' %(dk.info['number'], dk.info['name']))

    spinner.start(text='正在为您打卡打卡打卡')
    res = dk.post()
    if str(res['e']) == '0':
        spinner.stop_and_persist(symbol='🦄 '.encode('utf-8'), text='已为您打卡成功！')
    else:
        spinner.stop_and_persist(symbol='🦄 '.encode('utf-8'), text=res['m'])


if __name__=="__main__":
    if os.path.exists('./config.json'):
        configs = json.loads(open('./config.json', 'r').read())
        username = configs["username"]
        password = configs["password"]
        hour = configs["schedule"]["hour"]
        minute = configs["schedule"]["minute"]
    else:
        username = input("👤 浙大统一认证用户名: ")
        password = getpass.getpass('🔑 浙大统一认证密码: ')
        print("⏲  请输入定时时间（默认每天6:05）")
        hour = input("\thour: ") or 6
        minute = input("\tminute: ") or 5

    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', args=[username, password], hour=hour, minute=minute)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass