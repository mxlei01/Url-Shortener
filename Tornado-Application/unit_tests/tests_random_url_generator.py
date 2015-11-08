import tornado
import urlparse
from tornado.testing import AsyncTestCase
from random_url_generator.random_url_generator import AsyncRandomURLGenerator
from random_url_generator.random_url_settings import length_url

class TestURLGenerator(AsyncTestCase):
    @tornado.testing.gen_test
    def test_url_generated_length(self):
        # Usage:
        #       Test Case to determine if the url is in generated length
        # Arguments:
        #       None

        # Create a url generator
        url_generator = AsyncRandomURLGenerator()

        # Generate a new URL
        url = yield url_generator.generate_url()

        # Test to see if the generated path is equal to the length defined in
        # random_url_settings.py
        self.assertEqual(len(urlparse.urlsplit(url).path)-1, length_url)