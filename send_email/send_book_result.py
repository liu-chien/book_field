from send_email.email_account import sender_email, sender_passwd, receiver_email
from send_email.send_email import send_email


def send_book_result(date, time, counter,
                     sender_email=sender_email,
                     sender_passwd=sender_passwd,
                     receiver_email=receiver_email,
                    ):
    message = '''\
Subject: Booking Result

{} field(s) are reserved.
Date: {}
Time: {}:00
    '''.format(counter, date, time)

    send_email(message,sender_email,sender_passwd,receiver_email)
