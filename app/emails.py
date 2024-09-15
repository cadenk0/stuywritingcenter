import smtplib as smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lists import templates

class Emailer:
	
	def __init__(self, password='hckuompkvvjkqmzb'):
		self.password = password
		self.from_addr = 'stuywcwebsite@gmail.com@stuy.edu'

	def send(self, to_email, params, type='signup'):
		# to_email = "jlei60"
		conn = smtp.SMTP_SSL('smtp.gmail.com', 465)
		print(self.from_addr, self.password)
		conn.login(self.from_addr, self.password)
		template = templates[type]

		msg = MIMEMultipart('alternative')

		msg['Subject'] = template['subject'].format(
			params=params
		)
		msg['From'] = self.from_addr
		msg['To'] = to_email

		plain_text = MIMEText(template['plain'].format(params=params), 'plain')
		html = MIMEText(template['html'].format(params=params), 'html')
		msg.attach(plain_text)
		msg.attach(html)

		conn.sendmail(self.from_addr, to_email + '@nycstudents.net', msg.as_string())
		conn.close()

		print(msg.as_string())
