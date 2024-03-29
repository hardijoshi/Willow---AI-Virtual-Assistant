import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_whom, subject, content):
    sender_email = "hardi21062004@gmail.com"
    sender_pass = "tzmuybexzummwbnw"
    receiver_mail = to_whom

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_mail
        msg['Subject'] = subject
        msg.attach(MIMEText(content,'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email,sender_pass)
            server.sendmail(sender_email,receiver_mail,msg.as_string())
            print("email sent successfully")
    except Exception as e:
        print(f'Error: {e}')