import requests

def check_response(response):
    try:
        response.raise_for_status()
    except HTTPError as http_err:
        print('HTTP error occurred: {}'.format(http_err))  # Python 3.6
    except Exception as err:
        print('Other error occurred: {}'.format(err))  # Python 3.6
    else:
        print('Success!')

def check_result(text, key1='<script>alert', key2='</script></head>'):
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

def book_field(field_number, time_slot, date, account, passwd):
    '''
    Example:
        field_number = 1    # 第一場
        time_slot = 1       # 07:00-08:00
        date = 20191023     # 2019/10/23
    
    Return
        boolean. True if suceed.
    '''
    usr = {'account': account,'password': passwd}
    date = {'field': str(field_number), 'timeSlot': str(time_slot), 'account': account, 'date': str(date)}
    with requests.Session() as s:
        p = s.post('http://peo.nthu.edu.tw/nthugym/reservation/login_successfully.php', data=usr)
        r = s.post('http://peo.nthu.edu.tw/nthugym/reservation/reservAction.php', data=date)
        r.encoding = 'utf-8'

        return check_result(r.text)

if __name__ == '__main__':
    from account import account
    book_field(1, 1, '20191025', account['account'], account['password'])