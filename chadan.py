#coding=utf-8

from selenium import webdriver
import requests
import time
# from bs4 import BeautifulSoup
import json
import traceback
import threading
import ctypes
import inspect

class chadan_cls:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.operator = 'UNICOM'
        self.loopStatu = False
        self.certificationId = '97340'
        self.balance = 0
        self.orderId = ''

    def login(self, window, account, password):
        print('Try to login with {}:{}'.format(account,password))
        login_url = 'http://www.chadan.cn/loginIn'
        browser = self.webdriver
        browser.get(login_url)
        # time.sleep()
        username = browser.find_element_by_id('account')
        psw = browser.find_element_by_id('password')
        login_button = browser.find_element_by_id('loginButton')
        username.send_keys(account)
        psw.send_keys(password)
        login_button.click()
        print('3 seconds to get all arguments....')
        time.sleep(3)
        print('login successfully.')
        self.req = requests.Session() #构建Session
        cookies = browser.get_cookies() #导出cookie
        for cookie in cookies:
            print("{} : {}".format(cookie['name'],cookie['value']))
            self.req.cookies.set(cookie['name'],cookie['value']) #转换cookies
            if cookie['name'] == 'logged':
                self.logged = cookie['value']
        self.create_getdan_task(window)

    def create_getdan_task(self, window):
        try:
            self.t = threading.Thread(target=self.getdan_task, args=(window, ), name='GetDan')
        except BaseException as e:
            # print(str(e))
            msg = traceback.format_exc()
            print (msg)
        self.t.start()

    def getBalance(self, window):
        post_url = 'http://www.chadan.cn/user/getBalance'
        test_data ={'JSESSIONID' : self.logged}
        response = self.req.post(post_url,data=test_data)
        if response.status_code != 200:
            # print('response.status_code = {}'.format(response.status_code))
            return 0

        # print('response.text : {}'.format(response.text))
        try :
            resp_json = json.loads(response.text)
        except BaseException as e:
            # print('response.text : {}'.format(response.text))
            msg = traceback.format_exc()
            # print(msg)
            # if 'errorMsg' not in resp_json:
            #     print('resp_json:{}'.format(resp_json))
            #     return False
        if resp_json['errorMsg'] == 'OK':
            # print('data = {}'.format(resp_json['data']))
            data_in_response = resp_json['data']
            # print(type(data_in_response))
            # print(data_in_response)
            if len(data_in_response):
                # print(type(data_in_response['balance']))
                # print(data_in_response['balance'])
                self.balance = data_in_response['balance']
                return data_in_response['balance']
        return 0

    def get_dan(self, window, operator, num):
        post_url = 'http://api.chadan.wang/order/getOrderdd623299'
        test_data ={'JSESSIONID' : self.logged,
                    'faceValue' : num,
                    'province':'',
                    'amount':'1',
                    'operator':operator,
                    'channel':'1'}
        print('Try to get {} {}...'.format(operator, num))
        response = self.req.post(post_url,data=test_data)
        if response.status_code != 200:
            print('response.status_code = {}'.format(response.status_code))
            return False

        # print('response.text : {}'.format(response.text))
        # resp_json = []
        try :
            resp_json = json.loads(response.text)
        except BaseException as e:
            # print('response.text : {}'.format(response.text))
            msg = traceback.format_exc()
            print(msg)
            # if 'errorMsg' not in resp_json:
            #     print('resp_json:{}'.format(resp_json))
            #     return False
        if resp_json['errorMsg'] == 'OK':
            # print('data = {}'.format(resp_json['data']))
            data_in_response = resp_json['data']
            print(type(data_in_response))
            print(data_in_response)
            if len(data_in_response):
                print(type(data_in_response[0]))
                print(data_in_response[0])
                window.dan_statu.setText('成功')
                self.orderId = data_in_response[0]['id']
                print(data_in_response[0]['rechargeAccount'])
                print(data_in_response[0]['cutOffTime'])
                window.dan_info_phone.setText('手机号码：' + data_in_response[0]['rechargeAccount'][0:3] + '-' + data_in_response[0]['rechargeAccount'][3:7] +'-'+ data_in_response[0]['rechargeAccount'][7:11])
                # window.dan_info_deadtime.setText('截止时间：' + data_in_response[0]['cutOffTime'])
                return True
        return False

    def getdan_task(self, window):
        i = 1
        while True:
            # print('Try to get {} {} {}dan'.format(arg,arg2,arg3))
            time.sleep(0.25)
            if self.loopStatu == False:
                self.balance = self.getBalance(window)
                # print(blance)
                if self.balance > 0:
                    self.withdrawApply()
                # window.cash.setText(str(blance))
                print('Stop!')
                continue
            else:
                window.dan_info_phone.setText('null')
                # window.dan_info_deadtime.setText('')
            arg = window.dan_lineEdit.text()
            if i == 1:
                window.dan_statu.setText('正在获取..')
            elif i== 2:
                window.dan_statu.setText('正在获取....')
            elif i == 3:
                window.dan_statu.setText('正在获取......')
            else:
                window.dan_statu.setText('出错了！')
                return
            if i == 3:
                i = 1
            else:
                i += 1

            if window.checkBox_mobile.isChecked() :
                if self.get_dan(window, 'MOBILE', arg):
                    print('Get dan MOBILE successfully!')
                    self.loopStatu = False
                time.sleep(0.15)
            if window.checkBox_unicom.isChecked() :
                if self.get_dan(window, 'UNICOM', arg):
                    print('Get dan MOBILE successfully!')
                    self.loopStatu = False

    def startdan(self):
        self.loopStatu = True
        # 启动个2分钟的计时器，自动提交订单
        # time.sleep(120)
        # self.commitdan()

    def stopdan(self):
        self.loopStatu = False

    def commitdan(self):
        post_url = 'http://www.chadan.cn/order/confirmOrderdd623299'
        test_data ={'JSESSIONID' : self.logged,
                    'id' : self.orderId,
                    'orderStatus':1,
                    'submitRemark':''}
        # print('Try to get {} {}...'.format(operator, num))
        response = self.req.post(post_url,data=test_data)
        if response.status_code != 200:
            print('response.status_code = {}'.format(response.status_code))
            return False
        return True

    def withdrawApply(self):
        post_url = 'http://www.chadan.cn/withdraw/withdrawApply'
        test_data = {'JSESSIONID': self.logged,
                     'certificationId': self.certificationId,
                     'withdrawType': 1,
                     'price': self.balance}
        # print('Try to get {} {}...'.format(operator, num))
        response = self.req.post(post_url, data=test_data)
        if response.status_code != 200:
            print('response.status_code = {}'.format(response.status_code))
            return False
        return True

    def logout(self):
        self.webdriver.quit()
        self.req.close()
