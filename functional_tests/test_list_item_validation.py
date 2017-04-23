from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
import time

from unittest import skip

class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Edit goes to the home page and accidentially tries to submit
        # an empty list item. She hits enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # the browser intercepts the request, and does not load the list page
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # she starts typing some text for the new item and the error disappears
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # and she can submit it sucessfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # again, the browser will not comply
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            "#id_text:invalid"
        ))

        # and she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # edith gos to the homepage and starts a new list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy wellies')

        # she accidentially tries to enter a duplicate item
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # she sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        # edit starts a list a causes a validation error
        self.browser.get(self.live_server_url)
        self.add_list_item('Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # she starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # she is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
