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

## Example
To book field on 2021/02/05 18:00-19:00
```
python book.py -d 20210205 -t 18
```

To select field priority, add ```-o``` flag. <br>
E.g. to book field number 1, 4, 5, 6, 7 in order.
```
python book.py -d 20210205 -t 18 -o 14567
```

