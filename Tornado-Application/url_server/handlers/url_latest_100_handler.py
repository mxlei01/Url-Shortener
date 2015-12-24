import tornado.web
from tornado import gen
from tornado.escape import json_encode

class URLLatest100Handler(tornado.web.RequestHandler):
    def initialize(self, db, cursor_parser, executor, logger):
        # Usage:
        #       constructor for the URLLatest100Handler class, usage is primary setting
        #       the cursor_parser and db connector (momoko), and an executor to help
        # Arguments:
        #       db            (object) : a AsyncMomokoDBQueryExecutor object that uses
        #                                the momoko module to read and write to a Postgres db
        #       cursor_parser (object) : a AsyncSQLDataParser object to help with getting data
        #                                from a cursor asynchronously
        #       executor      (object) : an executor thread pool object to help us run
        #                                synchronous methods
        #       logger        (object) : a logger module
        # Return:
        #       None

        self.db = db
        self.cursor_parser = cursor_parser
        self.executor = executor
        self.logger = logger

    @gen.coroutine
    def get(self):
        # Usage:
        #       This function gets a get request, and will return the latest 100 shortened urls.
        # Arguments:
        #       None
        # Return:
        #       Json : a json format dictionary of original url

        # Get the latest 100 shortened url's cursor
        get_latest_100_shortened_urls = yield self.db.get_latest_100_shortened_urls()

        # We will use the cursor to extract the data using the cursor_parser
        get_latest_100_shortened_urls_data = yield self.cursor_parser.submit_get_data(get_latest_100_shortened_urls)

        # Use an executor to do any CPU bound tasks if possible to not block the IOLoop
        latest_urls = yield self.executor.submit(self.get_shortened_url_array, get_latest_100_shortened_urls_data)

        # Return the json encoded form of a an array of (shortened_url, date) tuples
        self.write(json_encode(dict(latest_100_shortened_urls=latest_urls)))

    def get_shortened_url_array(self, latest_100_shorted_url):
        # Usage:
        #       This function gets a get request, and will return the latest 100 shortened urls.
        # Arguments:
        #       None
        # Return:
        #       Array : array of latest 100 (shortened_url, date) tuple in sorted order

        # Create an array that returns a shortened_url by getting the "shortened_url" key
        # inside each dictionary for each element in the array.
        return [dict(shortened_url=shortened_url["shortened_url"], date=str(shortened_url["date"])) for shortened_url in latest_100_shorted_url]