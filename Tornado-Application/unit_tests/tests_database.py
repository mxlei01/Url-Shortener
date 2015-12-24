import tornado
import datetime
import momoko
from tornado.testing import AsyncTestCase
from url_server.database_access_momoko import momoko_settings
from url_server.database_access_momoko.momoko_query_executor import AsyncMomokoDBQueryExecutor
from url_server.handler_helpers.sql_cursor_parser import AsyncSQLDataParser

class TestDB(AsyncTestCase):
    #   Usage:
    #       Tests for database functions, such as read/write. This class inherits from the
    #       AsyncTestCase class in order to test coroutines, and futures.

    def setUp(self):
        # Usage:
        #       Constructor for TestDB, primarly for setting up the momoko pool, and cursor parser
        #       so later in other unit tests, we can use them
        # Arguments:
        #       None

        # Need to call parent's setup
        super(TestDB, self).setUp()

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

        # A few dummy variables to test our database with
        self.dummy_shortened_url = "dummy_shortened_url"
        self.dummy_original_url = "dummy_original_url"
        self.dummy_domain = "dummy_domain"
        self.dummy_time = datetime.datetime.now().isoformat()

    @tornado.testing.gen_test
    def test_00_test_db_insert_check_url(self):
        # Usage:
        #       Test Case to test if AsyncMomokoDBQueryExecutor can insert into url
        #       also can test AsyncSQLDataParser is able to get data from cursor
        # Arguments:
        #       None

        # Insert dummy data into url and url_info, since we don't actually want to
        # generate a url that can replace the real data we have in the postgres development server
        yield self.db.insert_new_mapping(self.dummy_shortened_url,
                                         self.dummy_original_url,
                                         self.dummy_time,
                                         self.dummy_domain)

        # Try to see if the shortened url exists by query it, this will return a cursor
        cursor = yield self.db.get_shortened_url(self.dummy_shortened_url)

        # We will use the cursor to extract the data using the cursor_parser
        dummy_data = yield self.cursor_parser.submit_get_data(cursor)

        # Assert that the data actually exists
        self.assertIsNotNone(dummy_data)

    @tornado.testing.gen_test
    def test_01_test_db_insert_check_url_info(self):
        # Usage:
        #       Test Case to test if our data is also inserted into url_info following the insertion
        #       to both url and url_info from test_00
        # Arguments:
        #       None

        # Try to see if the shortened url exists by query it, this will return a cursor
        cursor = yield self.db.get_shortened_url_info(self.dummy_shortened_url)

        # We will use the cursor to extract the data using the cursor_parser
        dummy_data = yield self.cursor_parser.submit_get_data(cursor)

        # Assert that the data actually exists
        self.assertIsNotNone(dummy_data)

    @tornado.testing.gen_test
    def test_02_test_db_delete_url(self):
        # Usage:
        #       Test case to see if the dummy data in url is deleted
        # Arguments:
        #       None

        # After we tested that the data is there, we need to remove the dummy url
        yield self.db.delete_shortened_url(self.dummy_shortened_url)

        # Try to see if the shortened url exists by query it, this will return a cursor
        cursor = yield self.db.get_shortened_url(self.dummy_shortened_url)

        # We will use the cursor to extract the data using the cursor_parser
        dummy_data = yield self.cursor_parser.submit_get_data(cursor)

        # Assert that the data is now deleted
        self.assertEqual(dummy_data, [])

    @tornado.testing.gen_test
    def test_03_test_db_delete_url_info(self):
        # Usage:
        #       Test case to see if the dummy data in url_info is deleted
        # Arguments:
        #       None

        # Try to see if the shortened url exists by query it, this will return a cursor
        cursor = yield self.db.get_shortened_url_info(self.dummy_shortened_url)

        # We will use the cursor to extract the data using the cursor_parser
        dummy_data = yield self.cursor_parser.submit_get_data(cursor)

        # Assert that the data is now deleted
        self.assertEqual(dummy_data, [])