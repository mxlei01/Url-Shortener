from executor_thread_pool.executor import executor
from logger.logger import logger

class AsyncSQLDataParser(object):
    # Usage:
    #       This class is responsible for getting the data from the cursor asynchronously
    #       by submitting the task to an executor. Due to the fact that the data returned by the cursor
    #       can take a while to read, hence it's a good idea not to block the IOLoop.

    def __init__(self,
                 executor=executor,
                 logger=logger):
        # Usage:
        #       constructor for AsyncSQLDataParser
        # Arguments:
        #       executor    (object) : an executor object
        #       logger      (object) : a logger object
        # Return:
        #       None

        self.executor = executor
        self.logger = logger

    def submit_get_data(self, cursor):
        # Usage:
        #       This functions submits a function that gets the data from the cursor
        #       and returns the future.
        # Arguments:
        #       cursor (object) : cursor that contains the data
        # Return:
        #       future (object) :

        return self.executor.submit(self.get_data, cursor)

    def get_data(self, cursor):
        # Usage:
        #       This functions gets the data from the cursor, and forms an array of dictionary
        # Arguments:
        #       cursor (object): cursor that contains the data
        # Return:
        #       array : rows of data from the database

        # Each column in the description shows the name, then zip the data with their
        # column names by using fetchall()

        return [dict(zip([col[0] for col in cursor.description], row))
                             for row in cursor.fetchall()]