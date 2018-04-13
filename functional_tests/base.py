from urllib.parse import urlparse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from decouple import config
from datetime import datetime
import os
import time

MAX_WAIT = 10


def wait(fn):
	def modified_fn(*args, **kwargs):
		start_time = time.time()
		while True:
			try:
				return fn(*args, **kwargs)
			except(WebDriverException, AssertionError) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e;
				time.sleep(0.5)
	return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		if config('DOCKER_IP', default=''):
			cls.host = config('DOCKER_IP')
		super(FunctionalTest, cls).setUpClass()

	def getRemoteBrowser(self):
		capabilities = DesiredCapabilities.FIREFOX.copy()
		capabilities.update({'logLevel': 'ERROR'})
		jenkins_server = urlparse(config('JENKINS_URL'))
		remote_server = jenkins_server.scheme + '://' + jenkins_server.hostname + ':4444/wd/hub'

		return webdriver.Remote(
			command_executor=remote_server, 
			desired_capabilities=capabilities
		)		

	def setUp(self):
		if config('JENKINS_URL', default=''):
			self.browser = self.getRemoteBrowser()
			self.screenshots_path = '/{0}/{1}'.format(
				'screenshots', 
				config('BUILD_TAG')
			)
		else:
			self.browser = webdriver.Firefox()
			self.screenshots_path = os.path.join(
			    os.path.dirname(os.path.abspath(__file__)), 'screenshots'
			)

		self.staging_server = config('STAGING_SERVER', default='')
		if self.staging_server:
			self.live_server_url = 'http://' + self.staging_server

	def tearDown(self):
		if self._test_has_failed():
			if not os.path.exists(self.screenshots_path):
				os.makedirs(self.screenshots_path)
			for ix, handle in enumerate(self.browser.window_handles):
				self._windowid = ix
				self.browser.switch_to_window(handle)
				self.take_screenshot()
				self.dump_html()

		self.browser.quit()
		super().tearDown()

	def _test_has_failed(self):
		return any(error for (method, error) in self._outcome.errors)

	def take_screenshot(self):
		filename = self._get_filename() + '.png'
		print('Saving screenshot to {}'.format(filename))
		self.browser.get_screenshot_as_file(filename)

	def dump_html(self):
		filename = self._get_filename() + '.html'
		print('Saving HTML contents to {}'.format(filename))
		with open(filename, 'w') as f:
			f.write(self.browser.page_source)

	def _get_filename(self):
		timestamp = datetime.now().isoformat().replace(':', '.')[:19]
		return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
			folder=self.screenshots_path,
			classname=self.__class__.__name__,
			method=self._testMethodName,
			windowid=self._windowid,
			timestamp=timestamp
		)

	def click_and_send_keys(self, element_id, keys_to_send):
		element_id.click()
		element_id.send_keys(keys_to_send)

	def click_and_submit_keys(self, element_id, keys_to_send):
		self.click_and_send_keys(element_id, keys_to_send)
		element_id.send_keys(Keys.ENTER)
	
	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')

	def add_list_item(self, item_text):
		num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
		self.click_and_submit_keys(self.get_item_input_box(), item_text)
		item_number = num_rows + 1
		self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

	@wait
	def wait_for(self, fn):
		return fn()

	@wait
	def wait_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	@wait
	def wait_to_be_logged_in(self, email):
		self.browser.find_element_by_link_text('Log out')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)

	@wait
	def wait_to_be_logged_out(self, email):
		self.browser.find_element_by_name('email')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)
