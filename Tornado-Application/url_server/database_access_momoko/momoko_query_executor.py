import momoko_pool
from tornado import gen
from logger.logger import logger

class AsyncMomokoDBQueryExecutor(object):
    # Usage:
    #       This class is responsible for DB reads and writes. It will use the momoko_db_connection
    #       that is created in momoko_pool to access a postgres DB.

    def __init__(self,
                 momoko_pool=momoko_pool.momoko_db_connection,
                 logger=logger):
        # Usage:
        #       constructor for AsyncMomokoDBQueryExecutor
        # Arguments:
        #       momoko_pool (object) : a momoko pool object that can be used to access a postgres DB
        #       logger      (object) : a logger object
        # Return:
        #       None

        self.momoko_pool = momoko_pool
        self.logger = logger

    @gen.coroutine
    def insert_new_mapping(self, shortened_url, original_url, date, domain, count_visited=0):
        # Usage:
        #       This function adds new shortened_url and original_url mappings
        # Arguments:
        #       shortened_url (string) : the shortened version of the original url
        #       original_url  (string) : the original url
        #       date          (string) : the date that the shortened_url is added
        #       domain        (string) : the domain of the original url
        #       count_visited (int)    : counter that sets the amount of times the shortened url is visited
        # Return:
        #       future_array  (array)  : array of futures that contains the cursors

        # First insert statement to insert a new pair of shortened_url and original_url
        insert_url = """
            INSERT INTO url (shortened_url, original_url)
            VALUES (%s, %s)
        """

        # Second insert statement to insert information of the shortened_url, such as
        # count_visited, date, and domain
        insert_url_info = """
            INSERT INTO url_info (shortened_url, count_visited, date, domain)
            VALUES (%s, %s, %s, %s)
        """

        # Executions both insertions in parallel
        future_array = yield [self.momoko_pool.execute(insert_url, (shortened_url, original_url)),
                              self.momoko_pool.execute(insert_url_info, (shortened_url, count_visited, date, domain))]

        self.logger.info("insert_url:%s, insert_url_info:%s, shortened_url:%s, "
                         "original_url:%s, date:%s, domain:%s, count_visited:%s, inserted"
                         % (insert_url, insert_url_info, shortened_url, original_url, date, domain, count_visited))

        raise gen.Return(future_array)

    @gen.coroutine
    def get_shortened_url(self, shortened_url):
        # Usage:
        #       This function returns the url given the shorted_url
        # Arguments:
        #       shortened_url (string) : the shortened version of the original url
        # Return:
        #       future        (cursor) : a future that contains a cursor

        # get statement to select a rows where url = shortened_url
        get_url = """
            SELECT *
            FROM url
            WHERE shortened_url=%s
        """

        # Execute the statement using the momoko pool
        future = yield self.momoko_pool.execute(get_url, (shortened_url,))

        self.logger.info("shortened_url:%s, selected" % (shortened_url))

        raise gen.Return(future)

    @gen.coroutine
    def get_shortened_url_info(self, shortened_url):
        # Usage:
        #       This function returns the url given the shorted_url's info
        # Arguments:
        #       shortened_url (string) : the shortened version of the original url
        # Return:
        #       future        (cursor) : a future that contains a cursor

        # get statement to select a rows where url = shortened_url
        get_url_info = """
            SELECT *
            FROM url_info
            WHERE shortened_url=%s
        """

        # Execute the statement using the momoko pool
        future = yield self.momoko_pool.execute(get_url_info, (shortened_url,))

        self.logger.info("shortened_url:%s, selected" % (shortened_url))

        raise gen.Return(future)


    @gen.coroutine
    def delete_shortened_url(self, shortened_url):
        # Usage:
        #       This function returns the url given the shorted_url
        # Arguments:
        #       shortened_url (string) : the shortened version of the original url
        # Return:
        #       future        (cursor) : a future that contains a cursor

        # delete statement to delete the shortened url
        delete_url = """
            DELETE from url
            WHERE shortened_url=%s
        """

        # Execute the statement using the momoko pool
        future = yield self.momoko_pool.execute(delete_url, (shortened_url,))

        self.logger.info("shortened_url:%s, deleted" % (shortened_url))

        raise gen.Return(future)