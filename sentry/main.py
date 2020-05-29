"""
# Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Security Sentry Program
# Made by Taian Chen
"""

try:
	print("[INFO]: Starting imports...")
	import configparser
	import smtplib
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	import imaplib
	from sys import exit as quit
except ImportError as ImportErrorMessage:
	configparser = lambda: exit(1)
	smtplib = lambda: exit(1)
	MIMEText = lambda: exit(1)
	MIMEMultipart = lambda: exit(1)
	imaplib = lambda: exit(1)
	quit = lambda: exit(1)
	print("[FAIL]: Imports failed! See below.")
	print(ImportErrorMessage)
	exit(1)
except ImportWarning as ImportWarningMessage:
	print("[FAIL]: Import warnings were raised! Please proceed with caution, see below for more details.")
	print(ImportWarningMessage)
pass

class sentry:
	"""
	Sentry program class.
	"""
	def __init__(self):
		"""
		Initiation function of Sentry.
		Declares variables and checks operation status, and if armed records environment for alarm triggers.
		"""
		print("[INFO]: Starting Sentry application...")
		print("[INFO]: Declaring variables...")
		self.is_armed = False
		print("[INFO]: Loading configuration...")
		configparser_load = configparser.ConfigParser()
		configparser_load.read("main.cfg")
		self.client_email = configparser_load["EMAIL"]["client_email"]
		self.host_email = [None, None]
		self.host_email[0] = configparser_load["EMAIL"]["host_email"]
		if "@gmail.com" not in self.host_email:
			print("[FAIL]: Host email is not registered under GMail, and is unsupported. Please replace with one.")
			quit(1)
		pass
		self.host_email[1] = configparser_load["EMAIL"]["host_key"]
		self.host_email[2] = self.host_email[0].rstrip("@gmail.com")
		while self.is_armed is False:
			sentry.client_send(self, "[raspbot] Sentry Control", "Hello user. \nReply to this email with commands to control Raspbot's Sentry program. "
		                                 "\nValid commands are: \narm - arms sentry\ndisarm - disarms sentry"
		                                 "\nrecording - returns audio recording from last alarm trigger "
		                                 "\nvideo - returns video recording from last alarm trigger "
		                                 "\nstop - stops sentry script, start again through SSH control of Raspbot"
		                                 "\nAny invalid commands will return a error message. \n \nThank you for using Raspbot Sentry. \n \n"
		                                 "\nRaspbot Project, by Taian Chen, MIT License since 2020"
		                                 "\nSee https://dreamerslegacy.xyz for documentation and more.")
		pass
	pass

	def client_send(self, subject, message):
		"""
		Sends a email to client.
		:param subject: subject line for email message.
		:param message: contents of message.
		:return: none.
		"""
		msg = MIMEMultipart()
		msg['From'] = self.client_email
		msg['To'] = self.host_email[0]
		msg['Subject'] = subject
		msg.attach(MIMEText(message, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		try:
			server.login(self.host_email[2], self.host_email[1])
		except smtplib.SMTPException:
			print("[FAIL]: Failed to login into host email.")
			# TODO add more advanced error handling, i.e close login and such
		pass
		text = msg.as_string()
		server.sendmail(self.host_email[0], self.client_email, text)
	pass

	def client_receive(self):
		"""
		Receives a email from client.
		:return: none. # TODO "'add return values' <- figure out why i left this todo because idk why i should return anything for this function" <- oh wait it needs to return the message received im dumb
		"""
		email_mapper = imaplib.IMAP4_SSL("imap.gmail.com")
		email_mapper.login(self.host_email[0], self.host_email[1])
		email_mapper.select("Inbox")
	pass
pass