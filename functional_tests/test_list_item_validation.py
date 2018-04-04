from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):
	def get_error_element(self):
		return self.browser.find_element_by_css_selector('.invalid-feedback')

	def click_and_send_keys(self, element_id, keys_to_send):
		element_id.click()
		element_id.send_keys(keys_to_send)

	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to submit
		# an empty list item. She hits Enter on the empty input box.
		self.browser.get(self.live_server_url)
		self.wait_for(
			lambda: self.click_and_send_keys(
				self.browser.find_element_by_id('id_text'), 
				Keys.ENTER
			)
		)

		# The browser intercepts the request, and does not load the 
		# list page
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))

		# She starts typing some text for the new item and the error disappears
		self.wait_for(
			lambda: self.click_and_send_keys(
				self.browser.find_element_by_id('id_text'), 
				'Buy milk'
			)
		)
		self.assertEqual(
			'Buy milk', 
			self.browser.find_element_by_id('id_text').get_attribute("value")
		)
		self.wait_for(
			lambda: self.browser.find_element_by_css_selector(
				'#id_text:valid'
			)
		)

		# And she can submit it successfully
		self.wait_for(
			lambda: self.click_and_send_keys(
				self.browser.find_element_by_id('id_text'), 
				Keys.ENTER
			)
		)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Perversely, she now decides to submit a second blank list item
		self.wait_for(
			lambda: self.click_and_send_keys(
				self.browser.find_element_by_id('id_text'), 
				Keys.ENTER
			)
		)
		
		# Again the browser will not comply
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for(
			lambda: self.browser.find_element_by_css_selector(
				'#id_text:invalid'
			)
		)

		# And she can correct it by filling some text in
		self.wait_for(
			lambda: self.click_and_send_keys(
				self.browser.find_element_by_id('id_text'), 
				'Make tea'
			)
		)
		self.wait_for(
			lambda: self.browser.find_element_by_css_selector(
				'#id_text:valid'
			)
		)
		self.wait_for(
			lambda: self.click_and_send_keys(
				self.browser.find_element_by_id('id_text'), 
				Keys.ENTER
			)
		)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')

	def test_cannot_add_duplicate_items(self):
		# Edith goes to the home page and starts a new list
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy wellies')
		
		# She accidentally tries to enter a duplicate item
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		# She sees a helpful error message
		self.wait_for(lambda: self.assertEqual(
			self.get_error_element().text,
			"You've already got this item in your list"
		))
	
	
	def test_error_messages_are_cleared_on_input(self):
		# Edith starts a list and causes a validation error:
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('Banter too thick')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Banter too thick')
		self.get_item_input_box().send_keys('Banter too thick')
		self.get_item_input_box().send_keys(Keys.ENTER)

		self.wait_for(lambda: self.assertTrue(  
				self.get_error_element().is_displayed()  
		))

		# She starts typing in the input box to clear the error
		self.get_item_input_box().send_keys('a')

		# She is pleased to see that the error message disappears
		self.wait_for(lambda: self.assertFalse(
				self.get_error_element().is_displayed()  
		))