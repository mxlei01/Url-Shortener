import tornado
import momoko
import json
from url_server.router import router
from tornado.testing import AsyncHTTPTestCase
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

        # Return the application to our HTTP server
        return router.create_application(db=self.db,
                                         cursor_parser=self.cursor_parser)

    @tornado.testing.gen_test
    def test_00_url_generation(self):
        # Usage:
        #       Fetches a generated url from
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

        # Delete the shortened URL when we are done
        yield self.db.delete_shortened_url(json_response["shortened_url"])