import smtplib, ssl

def send_email(
    message,
    sender_email,
    sender_passwd,
    receiver_email,
    ):

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender_email, sender_passwd)
        server.sendmail(sender_email, receiver_email, message)
        print('Send mail to {} from {}'.format(receiver_email, sender_email))
