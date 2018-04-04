from decouple import config
import requests
import poplib
import time
import re

class ServerResponseException(Exception):
	def __init__(self, response_code, server_url, message):
		self.response_code = response_code
		self.server_url = server_url
		self.message = message


def create_session_on_server(base_url, test_email):
	test_session = requests.Session()
	try:
		server_response = test_session.get(base_url)
		if server_response.status_code != requests.codes.ok:
			raise ServerResponseException(server_response.status_code, base_url, 'Failed to get simple session.')

		if 'csrftoken' in test_session.cookies:
			csrftoken = test_session.cookies['csrftoken']
		else:
			raise Exception('Could not find csrftoken in test session.')

		email_data = dict(email=test_email, csrfmiddlewaretoken=csrftoken)
		email_link_url = base_url + '/accounts/send_login_email'
		server_response = test_session.post(email_link_url, data=email_data)
		if server_response.status_code != requests.codes.ok:
			raise ServerResponseException(server_response.status_code, email_link_url, 'Failed to request login email.')

		email_body = wait_for_email(test_email, 'Your login link for Superlists')
		if not email_body:
			raise Exception('Failed to get email from external email server.')

		url_search = re.search(r'http://.+/.+$', email_body)
		if not url_search:
			raise Exception('Could not find url in email body:\n{email_body}')

		login_url = url_search.group(0)
		server_response = test_session.get(login_url)
		if server_response.status_code != requests.codes.ok:
			raise ServerResponseException(server_response.status_code, login_url, 'Failed to login.')

		sessionid = test_session.cookies['sessionid']
		if not sessionid:
			raise Exception('Failed to get session ID from test session.')
		else:
			return sessionid
	except ServerResponseException as e:
		print(e.message + '\nStatus code:\t{0}\nServer URL:\t{1}'.format(e.response_code, e.server_url))		
	except Exception as e:
		print(e)


def wait_for_email(test_email, subject):

	email_id = None
	start = time.time()
	inbox = poplib.POP3_SSL('pop.mail.yahoo.com')
	try:
		inbox.user(test_email)
		inbox.pass_(config('YAHOO_PASSWORD', default=''))
		while time.time() - start < 60:
			# get 10 newest messages
			count, _ = inbox.stat()
			for i in reversed(range(max(1, count - 10), count + 1)):
				# print('getting msg', i)
				_, lines, __ = inbox.retr(i)
				lines = [l.decode('utf8') for l in lines]
				# print(lines)
				if f'Subject: {subject}' in lines:
					email_id = i
					body = '\n'.join(lines)
					return body
			time.sleep(5)
	except Exception as e:
		print(e)
		body = None
		return body
	finally:
		if email_id:
			inbox.dele(email_id)
		inbox.quit()