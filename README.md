# README
![os](https://img.shields.io/badge/Ubuntu-16.04-orange) ![python](https://img.shields.io/badge/Python-3.6-orange)

## Install required package
```
pip install -r requirements.txt
```

## Setting
1. Modify *account_example.py*. Fill in your own accont and password
2. Rename *account_example.py* to *account.py*</br>
   `mv account_example.py account.py`
3. Optional
   1. Modify *send_email/email_account_example.py*.
   2. Rename *send_email/email_account_example.py* to *send_email/email_account.py*</br>
   `mv send_email/email_account_example.py send_email/email_account.py`

## Example
Say one wants to book field on 2019/10/10 18:00
```
python script.py -d 20191110 -t 18
```
If one wants to send email to your account.
```
python script.py -d 20191110 -t 18 -e
```

## Advance
To change the field booking priority, modify *script.py line 22*

## ~~Alert~~
(Fixed on 2020/02/06)
The script is able to book the field which is <font color='red'>**不開放**</font>, make sure to check the available fields before running the script.
