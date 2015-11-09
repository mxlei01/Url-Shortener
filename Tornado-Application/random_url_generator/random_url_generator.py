import random_url_settings
import random
import urlparse
from tornado import gen
from executor_thread_pool.executor import executor
from logger.logger import logger

class AsyncRandomURLGenerator(object):
    # Usage:
    #       This class is responsible for generating a string of letters and digits randomly with a specified
    #       base, for example base 16 will include both numbers(0-9) and letters(A-F), and combine it
    #       with a domain_base.
    #       For example, if the domain base is http://mxlei01.com/url-shortener, and the generated
    #       shorted URL digits is 13EF0, then this class will output http://mxlei01.com/url-shortener/13ER90

    def __init__(self,
                 random_base=random_url_settings.random_base,
                 domain_base=random_url_settings.domain_base,
                 length_url=random_url_settings.length_url,
                 logger=logger,
                 executor=executor):
        # Usage:
        #       constructor for AsyncRandomURLGenerator
        # Arguments:
        #       random_base (array)  : array of numbers/letters
        #       domain_base (string) : a domain that we will attach our generated numbers to
        #       length_url  (int)    : a integer specifying the length of the shortened URL
        #       logger      (object) : a logger object
        #       executor    (object) : a executor object that allows to execute functions asynchronously
        # Return:
        #       None

        self.random_base = random_base
        self.domain_base = domain_base
        self.length_url = length_url
        self.logger = logger
        self.executor = executor

    @gen.coroutine
    def generate_url(self, change_to_url=None):
        # Usage:
        #       Function will use an executor to create a random path
        #       Then attaching it with domain_base using urlparse library.
        # Arguments:
        #       change_to_url (string) : a string containing a string that the user
        #                                want to use instead of a randomized string for
        #                                shortened url
        # Return:
        #       URL (future) : a future containing the result of the url shortening

        # See if the change_to_url exists, if it exists, then we want to use the
        # user's url instead of generating one ourselves
        if change_to_url:
            path = change_to_url
        else:
            # The path variable now contains a randomized string of self.length_url length
            path = yield self.executor.submit(self.generate_random_path)

        # Use the urlparse library to join the domain_base and the path to form a url
        url = urlparse.urljoin(self.domain_base, path)

        self.logger.info("Generated a URL:%s" % url)

        # Return a future containing the data of
        raise gen.Return(url)

    def generate_random_path(self):
        # Usage:
        #       Function when called with utilize self.random_base to generate a string of
        #       letters or numbers. The length of the string will be determined by the self.length_url.
        # Arguments:
        #       None
        # Return:
        #       URL (future) : a future containing the result of the url shortening

        return ''.join([random.choice(self.random_base) for _ in xrange(self.length_url)])