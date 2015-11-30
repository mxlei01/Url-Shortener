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

    @gen.coroutine
    def update_count(self, shortened_url, count):
        # Usage:
        #       This function updates the count of shortened_url access times in url_info table
        # Arguments:
        #       shortened_url (string) : the shortened version of the original url
        #       count         (int)    : count of shortened_url access times
        # Return:
        #       future        (cursor) : a future that contains a cursor

        # update statement to delete the shortened url
        update_count_url_info = """
            UPDATE url_info
            set count_visited = %s
            where shortened_url = %s
        """

        # Execute the statement using the momoko pool
        future = yield self.momoko_pool.execute(update_count_url_info, (count, shortened_url))

        self.logger.info("shortened_url:%s, updated with count:%d" % (shortened_url, count))

        raise gen.Return(future)

    @gen.coroutine
    def get_latest_100_shortened_urls(self):
        # Usage:
        #       This function gets the latest 100 shortened urls
        # Arguments:
        #       None
        # Return:
        #       future        (cursor) : a future that contains a cursor

        # Order by the date field, which is not a varchar in the table, but a date type
        # and limit by 100
        get_latest_100 = """
            select "shortened_url", "date"
            from url_info
            ORDER BY date DESC
            limit 100
        """

        # Execute the statement using the momoko pool
        future = yield self.momoko_pool.execute(get_latest_100, ())

        self.logger.info("Getting Latest 100 shortened URLs")

        raise gen.Return(future)

    @gen.coroutine
    def delete_all_records(self):
        # Usage:
        #       This function delete all records in the database
        # Arguments:
        #       None
        # Return:
        #       future        (cursor) : a future that contains a cursor

        # Order by the date field, which is not a varchar in the table, but a date type
        # and limit by 100
        delete_all = """
            DELETE from url
        """

        # Execute the statement using the momoko pool
        future = yield self.momoko_pool.execute(delete_all, ())

        self.logger.info("Deleting all records from the url database")

        raise gen.Return(future)

    @gen.coroutine
    def get_top_10_domain_in_30_days(self):
        # Usage:
        #       This function gets the top 10 popular domains in 30 days
        # Arguments:
        #       None
        # Return:
        #       future        (cursor) : a future that contains a cursor

        # This sql query counts the number of domains where we also
        # select that the days has to be in interval of 30 days. We then group by the domain
        # and order by the counts descending, then limit by 10.
        top_10_domain_in_30_days = """
            SELECT "domain", count("domain") as "counts"
            from url_info
            where "shortened_url" IN (SELECT "shortened_url"
                                      FROM url_info
                                      WHERE "date" > (CURRENT_DATE - INTERVAL '30 days'))
            group by "domain"
            ORDER BY "counts" DESC
            limit 10
        """

        # Execute the statement using the momoko pool
        future = yield self.momoko_pool.execute(top_10_domain_in_30_days, ())

        self.logger.info("Selecting the top 10 domain in 30 days")

        raise gen.Return(future)
