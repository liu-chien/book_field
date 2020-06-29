import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import pandas as pd

class Agent:
    def __init__(self, time_slot, date, account, passwd):
        self.usr = {'account': account,'password': passwd}
        self.data = {'field': None, 'timeSlot': str(time_slot), 'account': account, 'date': str(date)}
        print(self.data)
        self.sess = requests.Session()
        self.log_in()

    def log_in(self):
        p = self.sess.post('http://peo.nthu.edu.tw/nthugym/reservation/login_successfully.php', data=self.usr)
        self._check_response(p, 'Log in')

    def search_available_field(self):
        g = self.sess.get('http://peo.nthu.edu.tw/nthugym/reservation/reservation.php?date={}'.format(self.data['date']))
        return self._decode_available_field(g, self.data['timeSlot'])

    def _decode_available_field(self, g, timeSlot):
        self._check_response(g, 'Check available fields')
        soup = BeautifulSoup(g.text, 'html.parser')
        
        time_table = []                     # store all field status of the day
        all_tr = soup.find_all('tr')        # all imformation in the reservation table
        for row in all_tr:
            row_info = []                   # field status on a timeSlot
            for ele in row.find_all('td'):
                if ele.text == '':
                    row_info.append(ele.input['value'])
                else:
                    row_info.append(ele.text)
            time_table.append(row_info)
        
        time_table.pop(0)      # remove date which is an unnecessary information
        time_table = pd.DataFrame(time_table[1:], columns=time_table[0])
        # print(time_table)         # Debug

        field_status = time_table.loc[int(self.data['timeSlot'])-1, :].tolist()
        field_status.pop(0)               # remove timeSlot which is an unnecessary data

        available_field = []
        for i, status in enumerate(field_status):
            if status != '不開放':
                available_field.append(i+1)
        return available_field

    def book_field(self, field_number):
        self.data['field'] = str(field_number)
        r = self.sess.post('http://peo.nthu.edu.tw/nthugym/reservation/reservAction.php', data=self.data)
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
            print('請檢查帳號密碼是否正確')
            return None

    def _check_response(self, response, text):
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            print('HTTP error occurred: {}'.format(http_err))  # Python 3.6
        except Exception as err:
            print('Other error occurred: {}'.format(err))  # Python 3.6
        else:
            print('{} success!'.format(text))


# if __name__ == '__main__':
#     from account import account
#     book_field(1, 1, '20191025', account['account'], account['password'])