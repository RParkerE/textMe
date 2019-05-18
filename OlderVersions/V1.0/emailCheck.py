from imaplib import IMAP4, IMAP4_SSL

num = []
unread = []
failed = False

def read(hostname, username, password):
	hostname = 'imap.' + hostname 
	server = IMAP4_SSL(hostname)
	try:
		server.login(username, password)
		server.select('INBOX', readonly=True)
		msgnums = server.search(None, 'UnSeen')
		if(msgnums[0] == 'OK'):
			for num in msgnums[1]:
				unread.append(num[-1])
		else:
			unread.append(0)
	except IMAP4.error:
		failed = True
