import tornado
import urlparse
from tornado.testing import AsyncTestCase
from random_url_generator.random_url_generator import AsyncRandomURLGenerator
from random_url_generator.random_url_settings import length_url

class TestURLGenerator(AsyncTestCase):
    #   Usage:
    #       Tests for the random url generator. This class inherits from the
    #       AsyncTestCase class in order to test coroutines, and futures.

    def setUp(self):
        # Usage:
        #       Constructor for TestDB, TestURLGenerator,which is used for setting
        # Arguments:
        #       None

        # Need to call parent's setup
        super(TestURLGenerator, self).setUp()

        # Create a url generator
        self.url_generator = AsyncRandomURLGenerator()

    @tornado.testing.gen_test
    def test_00_url_generated_length(self):
        # Usage:
        #       Test Case to determine if the url is in generated length
        # Arguments:
        #       None

        # Generate a new URL
        url = yield self.url_generator.generate_url()

        # Test to see if the generated path is equal to the length defined in
        # random_url_settings.py
        self.assertEqual(len(urlparse.urlsplit(url).path.split("/")[-1]), length_url)

    @tornado.testing.gen_test
    def test_01_change_to_url(self):
        # Usage:
        #       Test Case to determine if the url is in generated length
        # Arguments:
        #       None

        # Change the last path to something else
        change_to_url = "Dummy"

        # Generate a new URL
        url = yield self.url_generator.generate_url(change_to_url)

        # Test to see if the generated path is equal to the length defined in
        # random_url_settings.py
        self.assertEqual(urlparse.urlsplit(url).path.split("/")[-1], change_to_url)