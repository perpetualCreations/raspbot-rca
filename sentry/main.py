"""
Raspbot Remote Control Application (Raspbot RCA, Raspbot RCA-G), v1.2
Security Sentry Program
Made by Taian Chen
"""

try:
	print("[INFO]: Starting imports...")
	import configparser
	import smtplib
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	import imaplib
	from sys import exit as stop
	import pyAudioAnalysis
except ImportError as ImportErrorMessage:
	configparser = lambda: exit(1)
	smtplib = lambda: exit(1)
	MIMEText = lambda: exit(1)
	MIMEMultipart = lambda: exit(1)
	imaplib = lambda: exit(1)
	stop = lambda: exit(1)
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
		self.run_loop = True
		print("[INFO]: Loading configuration...")
		configparser_load = configparser.ConfigParser()
		configparser_load.read("main.cfg")
		self.client_email = configparser_load["EMAIL"]["client_email"]
		self.host_email = [None, None]
		self.host_email[0] = configparser_load["EMAIL"]["host_email"]
		if "@gmail.com" not in self.host_email:
			print("[FAIL]: Host email is required to be a GMail address. Please replace entered address in configuration with one that is valid.")
			sentry.quit(self, 1)
		pass
		self.host_email[1] = configparser_load["EMAIL"]["host_key"]
		self.host_email[2] = self.host_email[0].rstrip("@gmail.com")
		print("[INFO]: Attempting to login into host email...")
		self.SMTP_service = smtplib.SMTP('smtp.gmail.com', 587)
		self.SMTP_service.ehlo()
		self.SMTP_service.starttls()
		try:
			self.SMTP_service.login(self.host_email[2], self.host_email[1])
		except smtplib.SMTPException as SMTPErrorMessage:
			print("[FAIL]: Failed to login into host email. See below for more information.")
			print(SMTPErrorMessage)
			sentry.quit(self, 1)
		pass
		print("[INFO]: Dispatching email to client...")
		sentry.client_send(self, "[raspbot] Sentry Control", "Hello user. \nReply to this email with commands to control Raspbot's Sentry program. "
								"\nValid commands are: \narm - arms sentry\ndisarm - disarms sentry"
								"\naudio - returns audio recording from last alarm trigger "
								"\nvideo - returns video recording from last alarm trigger "
								"\nstop - stops sentry script, start again through SSH control of Raspbot"
								"\nAny invalid commands will return a error message. \n \nThank you for using Raspbot Sentry. \n \n"
								"\nRaspbot Project, by Taian Chen, MIT License since 2020"
								"\nSee https://dreamerslegacy.xyz for documentation and more.")
		print("[INFO]: Listening to client...")
		while self.run_loop is True:
			while self.is_armed is True:
				# TODO start audio listening
				pass
			pass
			command = sentry.client_receive(self)
			if command == "arm":
				self.is_armed = True
				# TODO add additional logic from here
			elif command == "disarm":
				self.is_armed = False
				# TODO add additional logic from here
			elif command == "audio":
				# TODO add audio retrieval
				pass
			elif command == "video":
				# TODO add video retrieval
				pass
			elif command == "stop":
				# TODO additional stop logic
				sentry.quit(self, 0)
			else:
				# TODO add else case
				pass
			pass
			# TODO add audio processing for siren call
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
		self.SMTP_service.sendmail(self.host_email[0], self.client_email, msg.as_string())
	pass

	def client_receive(self):
		"""
		Receives a email from client.
		:return: Contents of received email message.
		"""
		try:
			email_mapper = imaplib.IMAP4_SSL("imap.gmail.com")
			email_mapper.login(self.host_email[0], self.host_email[1])
			email_mapper.select("Inbox")
		except imaplib.IMAP4.error:
			pass
		pass
		# TODO add imaplib read and output to email_contents
		email_contents = NotImplemented
		return email_contents
	pass

	def quit(self, exit_code):
		"""
		Wrapper for stop with additional instructions.
		:param exit_code: exit code for stop.
		:return: none.
		"""
		# TODO add any instructions here for quitting
		sentry.client_send(self, "[raspbot] Sentry Stopped", "Hello user. \nSentry has been stopped and is no longer running. "
		                        "\nRestart it with terminal. If you have not issued a stop command, its likely an error has occurred." 
		                        "\n \nThank you for using Raspbot Sentry. \n \n"
								"\nRaspbot Project, by Taian Chen, MIT License since 2020"
								"\nSee https://dreamerslegacy.xyz for documentation and more.")
		stop(exit_code)
	pass
pass
