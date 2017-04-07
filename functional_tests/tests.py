from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [ row.text for row in rows ])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise # coding=utf-8
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Sully heard about a cool new online to-do app. He goes to
        # check out the homepage
        self.browser.get(self.live_server_url)

        # he notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # he is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Hey types "Buy peacock feathers" into a text box (sully's hobby is
        # tying fly-fishing luers)
        inputbox.send_keys('Buy peacock feathers')

        # when he hits enter, the page updates, and now the page lists
        # "1: buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # there is still a text box invting him to add another item. he enters
        # "use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # the page updates again and now shows both items on his list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # sully wonders wheather the site will remember his list. Then he sees that
        # the ist has generated a unique url for him -- there is some explanator
        # text to that effect
        #self.fail("Finish the test!")
        # he visits his url - his to-do list is still there

        # satisfied, he goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # sully starts a new todo list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # he notices that his list has a unique url
        sully_list_url = self.browser.current_url
        self.assertRegex(sully_list_url, '/lists/.+')

        # now a new user, francis, comes to the site

        ## we use a new browser session to make sure no information of sully's
        ## list is coming though from cookies, etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # francis visits the homepage. there is no sign of sully's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # francis starts a new list by entering a new item. He is less interesting
        # than sully
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, sully_list_url)

        # again, no trace of sully's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # satisfied they both go back to sleep

    def test_layout_and_styling(self):
        # edit goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        # she notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # she starts a new list and sees the input is centerd on that page too
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

if __name__ == '__main__':
    unittest.main(warnings='ignore')
