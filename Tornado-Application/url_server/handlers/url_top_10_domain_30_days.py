import tornado.web
from tornado import gen
from tornado.escape import json_encode

class URLTop10Domain30Days(tornado.web.RequestHandler):
    def initialize(self, db, cursor_parser, logger):
        # Usage:
        #       constructor for the URLTop10Domain30Days class, usage is primary setting
        #       the cursor_parser and db connector (momoko), and an executor
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
        get_top_10_domain_30_days = yield self.db.get_top_10_domain_in_30_days()

        # We will use the cursor to extract the data using the cursor_parser
        get_top_10_domain_30_days_data = yield self.cursor_parser.submit_get_data(get_top_10_domain_30_days)

        # Return the json encoded form of a an array of (shortened_url, date) tuples
        self.write(json_encode(dict(top_10_domain_30_days=get_top_10_domain_30_days_data)))
