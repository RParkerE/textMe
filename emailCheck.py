#####################################################
#                                                   #
#                                                   #
#               emailCheck.py V2                    #
#               Author: RParkerE                    #
#               Date: 1/18/2016                     #
#                                                   #
#                                                   #
#####################################################

from imaplib import IMAP4, IMAP4_SSL

def read(hostname, username, password):
	# Get the imap server for the host
	hostname = 'imap.' + hostname.lower()
	# Start SSL connection with the host server
	server = IMAP4_SSL(hostname)
	try:
		# Login to the given account
		server.login(username, password)
		# Select the Inbox and make it read only
		server.select('INBOX', readonly=True)
		# Check how many unread messages are in the inbox
		msgnums = server.search(None, 'UnSeen')
		if(msgnums[0] == 'OK'):
			# List how many unread messages there are [1,2, 3, ...]
			for num in msgnums[1]:
				# Return number of unread messages (The last one in the list msgnums)
				return (num[-1])
		else:
			return ('Failed')
	except IMAP4.error:
		return ('Failed')
