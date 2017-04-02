from selenium import webdriver
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
        self.fail('Finish the test!')

        # he is invited to enter a to-do item straight away

        # Hey types "Buy peacock feathers" into a text box (sully's hobby is
        # tying fly-fishing luers)

        # when he hits enter, the page updates, and now the page lists
        # "1: buy peacock feathers" as an item in a to-do list

        # there is still a text box invting him to add another item. he enters
        # "use peacock feathers to make a fly"

        # the page updates again and now shows both items on his list

        # sully wonders wheather the site will remember his list. Then he sees that
        # the ist has generated a unique url for him -- there is some explanator
        # text to that effect

        # he visits his url - his to-do list is still there

        # satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')
