from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

from unittest import skip

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edit goes to the home page adn accidentially tries to submit
        # an empty list item. She hits enter on the empty input box

        # the home page refreshes, and there is an error message saying
        # that list items cannot be blank

        # she tries again with some text for hte item, which now works

        # perversely, she now decides to submit a second blank list item

        # she receives a similar warning on the list page

        # and she can correct it by filling some text in
        self.fail('write me!')
