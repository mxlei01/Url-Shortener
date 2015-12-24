import tornado.web
from tornado import gen
from tornado.escape import json_encode

class URLGetURLInfo(tornado.web.RequestHandler):
    def initialize(self, db, cursor_parser, logger):
        # Usage:
        #       constructor for the URLGetURLInfo class, usage is primary setting
        #       the cursor_parser and db connector (momoko)
        # Arguments:
        #       db            (object) : a AsyncMomokoDBQueryExecutor object that uses
        #                                the momoko module to read and write to a Postgres db
        #       cursor_parser (object) : a AsyncSQLDataParser object to help with getting data
        #                                from a cursor asynchronously
        #       logger        (object) : a logger module
        # Return:
        #       None

        self.db = db
        self.cursor_parser = cursor_parser
        self.logger = logger

    @gen.coroutine
    def get(self):
        # Usage:
        #       This function gets a get request, and will figure out what is the shortened url.
        #       From the shortened url, you can query the database to get the original url
        # Arguments:
        #       None
        # Return:
        #       Json : a json format dictionary of original url

        # Get the shortened_url based on the request
        shortened_url = self.get_argument('shortened_url')

        # Try to see if the shortened url exists by query it, this will return a cursor
        get_shortened_url = yield self.db.get_shortened_url_info(shortened_url)

        # We will use the cursor to extract the data using the cursor_parser
        get_shortened_url_data = yield self.cursor_parser.submit_get_data(get_shortened_url)

        # If the data returned is not empty, then the original_url will be the data
        # in the database. Otherwise, set it to None.
        if get_shortened_url_data:
            count = get_shortened_url_data[0]["count_visited"]
        else:
            count = None

        self.logger.info("shortened_url:%s, count:%s" % (shortened_url, count))

        # Return the json encoded form of a dictionary that contains the original url
        self.write(json_encode(dict(count=count)))