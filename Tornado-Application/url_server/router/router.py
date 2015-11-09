import tornado.web
from url_server.handlers.url_gen_handler import URLGenHandler
from url_server.handlers.url_redirect_handler import URLRedirectHandler
from url_server.database_access_momoko.momoko_query_executor import AsyncMomokoDBQueryExecutor
from url_server.handler_helpers.sql_cursor_parser import AsyncSQLDataParser
from random_url_generator.random_url_generator import AsyncRandomURLGenerator
from router_settings import settings
from logger.logger import logger as log

# url.py is used to map between different urls to handlers, and also to set different settings

# application is a tornado web application object, that can be used to set handlers, and settings
def create_application(url_generator=AsyncRandomURLGenerator(), db=AsyncMomokoDBQueryExecutor(),
                       cursor_parser=AsyncSQLDataParser(), logger=log):
    return tornado.web.Application([
        # Map the "/" url to main handler
        (r"/url_gen", URLGenHandler, dict(url_generator=url_generator,
                                          db=db,
                                          cursor_parser=cursor_parser,
                                          logger=logger)),
        (r'^/url_shortener/\w+', URLRedirectHandler, dict(db=db,
                                                       cursor_parser=cursor_parser,
                                                       logger=logger))
    ], **settings)
