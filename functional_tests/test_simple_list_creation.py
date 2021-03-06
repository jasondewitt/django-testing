from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Sully heard about a cool new online to-do app. He goes to
        # check out the homepage
        self.browser.get(self.live_server_url)

        # he notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # he is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
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
        self.add_list_item('Use peacock feathers to make a fly')

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
        self.add_list_item('Buy peacock feathers')

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
        self.add_list_item('Buy milk')

        # francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, sully_list_url)

        # again, no trace of sully's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # satisfied they both go back to sleep
