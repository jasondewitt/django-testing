from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Sully hearda bout a cool new online to-do app. He goes to
        # check out the homepage
        self.browser.get("http://localhost:8000")

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

        # there is still a text box invting him to add another item. he enters
        # "use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # the page updates again and now shows both items on his list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.assertIn(
            '2: Use peacock feathers to make a fly',
            [ row.text for row in rows ]
        )
        # sully wonders wheather the site will remember his list. Then he sees that
        # the ist has generated a unique url for him -- there is some explanator
        # text to that effect
        self.fail("Finish the test!")
        # he visits his url - his to-do list is still there

        # satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')
