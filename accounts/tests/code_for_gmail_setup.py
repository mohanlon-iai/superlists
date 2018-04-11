from decouple import config
from email import policy
from email.parser import BytesParser
import imaplib

# or maybe do this in setup?
def login_to_gmail():
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login('mohanlondev@gmail.com', config('EMAIL_PASSWORD', default=''))
	return mail
	
def get_email_with_login_link(subj_hash):
	try:
		mail = login_to_gmail()
		mail.select('inbox')

		type, msglist = mail.search(None, '(SUBJECT "Link to your Superlists account ")')
		
		msg_ids = msglist[0]
		msg_id = msg_ids.split()
		
		if len(msg_id) > 1:
			return None
		else:
			result, msg_data = mail.fetch(msg_id[0], '(RFC822)')
			for response_part in msg_data:
				if isinstance(response_part, tuple):
					msg = BytesParser(policy=policy.default).parsebytes(response_part[1])
					msg_content = msg.get_content()
					login_link = msg_content.strip()
					return login_link

	except Exception as e:
		print(e)
	finally:
		mail.logout()