import OpenSSL, sendgrid
import ssl, socket, os, smtplib, time, datetime
from sendgrid.helpers.mail import *
from datetime import timedelta

def sendMail(domain):
    email = os.environ.get('EMAIL_ADDRESS')
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(email)
    to_email = Email(email)
    subject = "SSL Cert for " + domain + " will expire soon"
    content = Content("text/plain", "SSL Cert for " + domain + " will expire soon")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

numDays = 30
now = time.time()
warnAfter = now + 86400*numDays

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '/domains') as f:
    domains = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
domains = [x.strip() for x in domains]

expired = []
timestamp = time.strftime("%c")
print ("Current time %s" % timestamp )

for domain in domains:
    print("%s - OK" % domain)
    cert=ssl.get_server_certificate((domain, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    notAfter = x509.get_notAfter()
    exp = time.mktime(datetime.datetime.strptime(notAfter, "%Y%m%d%H%M%SZ").timetuple())

    if(exp < warnAfter):
        sendMail(domain)
