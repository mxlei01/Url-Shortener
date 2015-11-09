import tornado.web
import datetime
import urlparse
import random
from tornado import gen
from tornado.escape import json_encode

class URLGenHandler(tornado.web.RequestHandler):
    def initialize(self, url_generator, db, cursor_parser, logger):
        # Usage:
        #       constructor for the URLGenHandler class, usage is primary setting
        #       the url_generator and db connector (momoko)
        # Arguments:
        #       url_generator (object) : a AsyncRandomURLGenerator object that uses
        #                                executors to generate a shortened URL
        #       db            (object) : a AsyncMomokoDBQueryExecutor object that uses
        #                                the momoko module to read and write to a Postgres db
        #       cursor_parser (object) : a AsyncSQLDataParser object to help with getting data
        #                                from a cursor asynchronously
        #       logger        (object) : a logger module
        # Return:
        #       None

        self.url_generator = url_generator
        self.db = db
        self.cursor_parser = cursor_parser
        self.logger = logger

    @gen.coroutine
    def post(self):
        # Usage:
        #       This function gets a post request, and it will generate new shortened URLs,
        #       and if the shortened URLs already exists, then delete the previous once
        # Arguments:
        #       None
        # Return:
        #       Json : a json format dictionary of shortened url, and original url


        # See if one of the parameters include a "change" parameter
        change_to_url = self.get_argument('change', None)

        # Generate a shortened url
        shortened_url = yield self.url_generator.generate_url(change_to_url)

        # Try to see if the shortened url exists by query it, this will return a cursor
        get_shortened_url = yield self.db.get_shortened_url(shortened_url)

        # We will use the cursor to extract the data using the cursor_parser
        get_shortened_url_data = yield self.cursor_parser.submit_get_data(get_shortened_url)

        # If the same shortened_url actually exists, then we need to delete it first
        # later we will add the shortened_url with the mapped url
        if get_shortened_url_data:
            yield self.db.delete_shortened_url(shortened_url)

        # Parse the url, this will give us the scheme, domain, netloc
        url = urlparse.urlparse(self.get_argument('url'))

        # Insert the new mapping into the database in both url, and url_info
        # if test is enabled, then we will swap the day with a random integer from 1 to 25
        if 'test' in self.request.body:
            date = datetime.datetime.now().replace(day=random.randint(1, 25)).isoformat()
        else:
            date = datetime.datetime.now().isoformat()
        yield self.db.insert_new_mapping(shortened_url,
                                         self.get_argument('url'),
                                         date,
                                         '%s://%s/'%(url.scheme, url.netloc))

        # Return a json format data that includes the shortened url and
        # the original url
        self.write(json_encode(dict(shortened_url=shortened_url,
                                    original_url=self.get_argument('url'))))