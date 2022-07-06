import smtplib, ssl
from secret import MAIL
from logFile import Status_Report



def send_update(subject,Emessage):
    port = MAIL.get('PORT')  # For starttls
    smtp_server = MAIL.get('SERVER')
    sender_email = MAIL.get('EMAIL')
    receiver_email =MAIL.get('EMAIL_TO')
    password = MAIL.get('PASSWORD')
    message = """\
    Subject: {0}

    {1}.""".format(subject,Emessage)
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        code="Mail Server Success"
        Rmessage = "Email sent"
        Status_Report(code,Rmessage)
    except BaseException as error:
        print(error)
        code="Mail Server Error"
        message = error
        Status_Report(code,message)

