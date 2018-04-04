from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from decouple import config
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
					print("Failed to execute function. Raising error: {}".format(e))
					raise e;
				time.sleep(0.5)
	return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.staging_server = config('STAGING_SERVER', default='')
		if self.staging_server:
			self.live_server_url = 'http://' + self.staging_server

	def tearDown(self):
		self.browser.refresh()
		self.browser.quit()

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
