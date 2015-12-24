import tornado
import momoko
import json
import urlparse
import datetime
import random
from tornado.testing import AsyncHTTPTestCase
from url_server.router import router
from url_server.database_access_momoko import momoko_settings
from url_server.database_access_momoko.momoko_query_executor import AsyncMomokoDBQueryExecutor
from url_server.handler_helpers.sql_cursor_parser import AsyncSQLDataParser

class TestURLGenHandler(AsyncHTTPTestCase):
    #   Usage:
    #       Tests for the url server, the difference from other tests is that
    #       this class inhereits from the AsyncHTTPTestCase class, which starts up
    #       a test server. Then we can use http_client to fetch webpages internally
    #       and check for their results.

    def get_app(self):
        # Usage:
        #       Constructor for TestURLGenHandler, we will need to return the
        #       application in order for the http server that starts up in this
        #       class to be called. We also need to setup a momoko_db_connection using
        #       the class's own io_loop like when we tested momoko pool in tests_database.py.
        # Arguments:
        #       None

        # The reason that we cannot use the same momoko_pool in momoko_pool.py is that
        # the unit tests generates it's own io_loop in the self.io_loop variable, hence
        # if we don't use it, momoko.pool isn't going to run on it's io_loop.
        self.momoko_db_connection = momoko.Pool(dsn='dbname=%s user=%s password=%s host=%s port=%s'
                                                    % (momoko_settings.dbname, momoko_settings.user,
                                                       momoko_settings.password, momoko_settings.host,
                                                       momoko_settings.port),
                                                size=momoko_settings.num_connections,
                                                ioloop=self.io_loop)

        # Call connect to establish connection with the momoko pool
        self.momoko_db_connection.connect()

        # Create an AsyncMomokoDBQueryExecutor so that we can use it's read/write functions
        self.db = AsyncMomokoDBQueryExecutor(momoko_pool=self.momoko_db_connection)

        # Create a cursor parser to get data from cursor
        self.cursor_parser = AsyncSQLDataParser()

        # Return the application to our HTTP server.
        return router.create_application(db=self.db,
                                         cursor_parser=self.cursor_parser)

    @tornado.testing.gen_test
    def test_00_url_generation(self):
        # Usage:
        #       Fetches a generated url from the /url_gen, which will give us a json response
        #       that contains both the shortened url and original url in the body. We will test
        #       if that shortened_url and original_url exists. Later on then delete the shortened_url
        #       from the database.
        # Arguments:
        #       None

        # A few variables to test on
        url_to_shorten = "http://www.google.com"

        # Get a response, which contains an url and original url
        response = yield self.http_client.fetch(self.get_url('/url_gen'), method='POST', body="url=%s" % (url_to_shorten))
        self.assertEqual(response.code, 200)

        # Test if the response's original_url is what we sent out
        json_response = json.loads(response.body)
        self.assertEqual(json_response["original_url"], url_to_shorten)

        # Test if the shortened_url exists
        self.assertIsNotNone(json_response["shortened_url"])

        # Delete the shortened URL when we are done
        yield self.db.delete_shortened_url(json_response["shortened_url"])

    @tornado.testing.gen_test
    def test_01_url_retrieve(self):
        # Usage:
        #       Fetches a generated url from the /url_gen, which will give us a json response
        #       that contains both the shortened url and original url in the body. We will visit the page
        #       using the shortened url. What we should observe is that we should get our original url,
        #       and then the count visited incremented.
        # Arguments:
        #       None

        # A few variables to test on
        url_to_shorten = "http://www.google.com"

        # Get a response, which contains an url and original url
        response = yield self.http_client.fetch(self.get_url('/url_gen'), method='POST', body="url=%s&test=true" % (url_to_shorten))
        self.assertEqual(response.code, 200)

        # Test if the response's original_url is what we sent out
        json_response = json.loads(response.body)
        self.assertEqual(json_response["original_url"], url_to_shorten)

        # Get a response, which will now contain url_info rows with count data
        response_info = yield self.http_client.fetch(self.get_url('/url_shortener/%s' % (urlparse.urlsplit(json_response["shortened_url"]).path.split("/")[-1])), method='GET')
        self.assertEqual(response_info.code, 200)

        # Try to see if the shortened url exists by query it, this will return a cursor
        get_url_info = yield self.db.get_shortened_url_info(json_response["shortened_url"])

        # We will use the cursor to extract the data using the cursor_parser
        get_url_info_data = yield self.cursor_parser.submit_get_data(get_url_info)

        # We need to make sure that the count is now +1
        self.assertEqual(get_url_info_data[0]["count_visited"], 1)

        # Delete the shortened URL when we are done
        yield self.db.delete_shortened_url(json_response["shortened_url"])

    @tornado.testing.gen_test
    def test_02_url_latest_100_fetch(self):
        # Usage:
        #       This will generate 100 URLS at random time
        # Arguments:
        #       None

        # Create a dummy url that we can shorten
        url_to_shorten = "http://www.google.com/"

        # Create 100 shortened URLs
        for fetch in xrange(100):
            # Get a response, which contains an url and original url
            yield self.http_client.fetch(self.get_url('/url_gen'), method='POST', body="url=%s&test=true" % (url_to_shorten))

        # Get a response, which will now contain 100 URLs in order
        response_info = yield self.http_client.fetch(self.get_url('/url_latest_100'), method='GET')
        json_response = json.loads(response_info.body)

        # For one date after another, the first date should always be greater than the second date
        for row in xrange(100):
            if row+1 < 100:
                time_1 = datetime.datetime.strptime(json_response["latest_100_shortened_urls"][row]["date"], "%Y-%m-%d %H:%M:%S.%f")
                time_2 = datetime.datetime.strptime(json_response["latest_100_shortened_urls"][row+1]["date"], "%Y-%m-%d %H:%M:%S.%f")
                self.assertTrue(time_1 >= time_2)

        # Delete all the records in the database
        yield self.db.delete_all_records()

    @tornado.testing.gen_test(timeout=20)
    def test_03_top_10_domain_30_days(self):
        # Usage:
        #       This will generate 100 URLS at random time
        # Arguments:
        #       None

        # We will create 10 different domains to test
        url_to_shorten_array = ["http://www.google%s.com/" % (num) for num in xrange(10)]

        # For each
        for url_to_shorten in url_to_shorten_array:
            # Create a random of 30 to 100 short_urls for each url_to_shorten
            for fetch in xrange(random.randint(30,100)):
                # Get a response, which contains an url and original url
                yield self.http_client.fetch(self.get_url('/url_gen'), method='POST', body="url=%s&test=true" % (url_to_shorten))

        # Get a response, which will now contain 10 domains in order
        response_info = yield self.http_client.fetch(self.get_url('/url_top_10_domain_30_days'), method='GET')
        json_response = json.loads(response_info.body)

        # For one date after another, the first date should always be greater than the second date
        for row in xrange(len(url_to_shorten_array)):
            if row+1 < len(url_to_shorten_array):
                self.assertTrue(json_response["top_10_domain_30_days"][row]["counts"] >=
                                json_response["top_10_domain_30_days"][row+1]["counts"])

        # Delete all the records in the database
        yield self.db.delete_all_records()

    @tornado.testing.gen_test
    def test_04_get_url_info(self):
        # Usage:
        #       Fetches a generated url from the /url_gen, and then we will url_info to get
        #       the data, and see if the dictionary is not empty.
        # Arguments:
        #       None

        # A few variables to test on
        url_to_shorten = "http://www.google.com"

        # Get a response, which contains an url and original url
        response = yield self.http_client.fetch(self.get_url('/url_gen'), method='POST', body="url=%s" % (url_to_shorten))

        # Test if the response's original_url is what we sent out
        json_response = json.loads(response.body)

        # Get a response, which will now contain 100 URLs in order
        response_info = yield self.http_client.fetch(self.get_url('/url_info?shortened_url=%s' % ((json_response["shortened_url"]))),
                                                     method='GET')
        json_response_info = json.loads(response_info.body)

        # See if the returned array is not none
        self.assertIsNotNone(json_response_info)

        # Delete the shortened URL when we are done
        yield self.db.delete_shortened_url(json_response["shortened_url"])

    @tornado.testing.gen_test
    def test_05_change_to_url(self):
        # Usage:
        #       Fetches a generated url from the /url_gen, which will give us a json response
        #       that contains both the shortened url and original url in the body. We will test
        #       if that shortened_url and original_url exists. Later on then delete the shortened_url
        #       from the database.
        # Arguments:
        #       None

        # Change the last path to something else
        change_to_url = "Dummy"

        # A url to shorten
        url_to_shorten = "http://www.google.com"

        # Get a response, which contains an url and original url
        response = yield self.http_client.fetch(self.get_url('/url_gen?change=%s' % (change_to_url)),
                                                method='POST', body="url=%s" % (url_to_shorten))

        # Test if the response's original_url is what we sent out
        json_response = json.loads(response.body)

        # Test if the shortened url's path is what we changed to
        self.assertIsNotNone(urlparse.urlsplit(json_response["shortened_url"]).path.split("/")[-1], change_to_url)
