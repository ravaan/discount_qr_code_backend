import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config import settings


def send_mail(zip_path, zip_name):

    message = MIMEMultipart()
    message['From'] = settings.FROM_ADDRESS
    message['To'] = settings.TO_ADDRESS
    message['Subject'] = "Here are your QR Codes"
    body = "Please find the QR Codes attached along with the mail"

    message.attach(MIMEText(body, 'plain'))

    filename = zip_name
    attachment = open(zip_path + zip_name, "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    message.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(settings.FROM_ADDRESS, settings.EMAIL_PASSWORD )

    text = message.as_string()
    s.sendmail(settings.FROM_ADDRESS, settings.TO_ADDRESS, text)
    s.quit()
