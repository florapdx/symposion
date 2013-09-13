from selenium import webdriver
import unittest

class NewVisitor(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_arrival(self):
        ## User visits homepage
        self.browser.get('http://localhost:8000')
        ## Sees correct site name
        self.assertIn('SymposionCon', self.browser.title)
        ## verify name
        print "Site title is " + self.browser.title

    def test_not_logged_in(self):
        ## Verify that new user doesn't see option to access dashboard
        self.assertNotIn('dashboard', self.browser.find_elements_by_link_text('dashboard'))

if __name__ == '__main__':
    unittest.main()