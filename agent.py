import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
# from PIL import Image
from io import BytesIO
import random


class Agent:
    def __init__(self):
        self.user = {'account': None, 'password': None, 'captcha_code': None}
        self.data = {'field': None, 'timeSlot': None, 'account': None, 'date': None}
        self.sess = requests.Session()

    # def get_captcha_code(self, scale=3, test=False):
    #     g = self.sess.get(
    #         "http://peo.nthu.edu.tw/nthugym/reservation/securimage/securimage_show.php")
    #     img = Image.open(BytesIO(g.content))
    #     new_size = [var*scale for var in img.size]
    #     if not test:
    #         img = img.resize(new_size)
    #         img.show()
    #         self.user["captcha_code"] = input("Type the arithmetic result: ")
    #     return img

    def log_in(self, account, passwd):
        self.user['account'] = account
        self.user['password'] = passwd
        self.data['account'] = account
        # self.get_captcha_code()     # fill in self.user['captcha_code]
        self.data['captcha_code'] = random.randint(0, 20)
        p = self.sess.post(
            'http://peo.nthu.edu.tw/nthugym/reservation/login_successfully.php',
            data=self.user)
        return p

    def search_available_field(self, date, timeSlot):
        self.data['date'] = str(date)
        self.data['timeSlot'] = str(timeSlot)
        g = self.sess.get(
            'http://peo.nthu.edu.tw/nthugym/reservation/reservation.php?date={}'.format(
                self.data['date']))
        return self._decode_available_field(g, timeSlot)

    def _decode_available_field(self, g, timeSlot):
        '''
        timeSlot: 1 -> 07:00-08:00, 2 -> 08:00-09:00
        '''
        # self._check_response(g, 'Check available fields')
        g.encoding = 'utf-8'
        soup = BeautifulSoup(g.text, 'html.parser')
        time_table = []                     # store all field status of the day
        # all imformation in the reservation table
        all_tr = soup.find_all('tr')
        for row in all_tr:
            row_info = []                   # field status on a timeSlot
            for ele in row.find_all('td'):
                if ele.text == '':
                    row_info.append(ele.input['value'])
                else:
                    row_info.append(ele.text)
            time_table.append(row_info)
        # remove date which is an unnecessary information
        time_table.pop(0)
        time_table = pd.DataFrame(time_table[1:], columns=time_table[0])
        # print(time_table)         # Debug

        field_status = time_table.loc[int(self.data['timeSlot'])-1, :].tolist()
        # remove timeSlot which is an unnecessary data
        # print(field_status)         # Debug
        field_status.pop(0)

        available_field = []
        
        for i, status in enumerate(field_status):
            if status != '不開放':
                available_field.append(i+1)
        return available_field

    def book_field(self, date, timeSlot, field_number):
        self.data['date'] = date
        self.data['timeSlot'] = timeSlot
        self.data['field'] = str(field_number)
        r = self.sess.post(
            'http://peo.nthu.edu.tw/nthugym/reservation/reservAction.php', data=self.data)
        r.encoding = 'utf-8'
        return self._check_result(r.text)

    def _check_result(self, text, key1='<script>alert', key2='</script></head>'):
        text = text[1100:1300]
        start = text.find(key1)
        end = text.find(key2)
        result = text[start+len(key1):end]
        if len(result) == 15:       # ('已經有人預約或尚未開放') or ('同一時段只能預借兩個場')
            print(result)
            return False
        elif len(result) == 40:     # ("預約成功!提醒您~ 進入球場前請在大廳換上室內運動鞋，且禁穿黑色膠底鞋。")
            print(result)
            return True
        else:
            print(result)
            return None

    # def _check_response(self, response, text):
    #     try:
    #         response.raise_for_status()
    #     except HTTPError as http_err:
    #         print('HTTP error occurred: {}'.format(http_err))  # Python 3.6
    #     except Exception as err:
    #         print('Other error occurred: {}'.format(err))  # Python 3.6
    #     else:
    #         print('{} success!'.format(text))