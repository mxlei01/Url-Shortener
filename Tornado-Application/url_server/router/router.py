import tornado.web
import router_settings
from random_url_generator.random_url_generator import AsyncRandomURLGenerator
from router_settings import settings
from logger.logger import logger as log
from executor_thread_pool.executor import executor as executors
from url_server.database_access_momoko.momoko_query_executor import AsyncMomokoDBQueryExecutor
from url_server.handler_helpers.sql_cursor_parser import AsyncSQLDataParser
from url_server.handlers.url_gen_handler import URLGenHandler
from url_server.handlers.url_redirect_handler import URLRedirectHandler
from url_server.handlers.url_latest_100_handler import URLLatest100Handler
from url_server.handlers.url_top_10_domain_30_days import URLTop10Domain30Days
from url_server.handlers.url_get_url_info import URLGetURLInfo

# url.py is used to map between different urls to handlers, and also to set different settings

# application is a tornado web application object, that can be used to set handlers, and settings
def create_application(url_generator=AsyncRandomURLGenerator(), db=AsyncMomokoDBQueryExecutor(),
                       cursor_parser=AsyncSQLDataParser(), logger=log, executor=executors,
                       url_shortener_path=router_settings.url_shortener_path):
    return tornado.web.Application([
        # Map the "/" url to main handler
        (r"/url_gen", URLGenHandler, dict(url_generator=url_generator,
                                          db=db,
                                          cursor_parser=cursor_parser,
                                          url_shortener=url_shortener_path,
                                          logger=logger)),
        (r'^%s\w+' % url_shortener_path, URLRedirectHandler, dict(db=db,
                                                                                  cursor_parser=cursor_parser,
                                                                                  logger=logger)),
        (r'^/url_latest_100', URLLatest100Handler, dict(db=db,
                                                        cursor_parser=cursor_parser,
                                                        executor=executor,
                                                        logger=logger)),
        (r'^/url_top_10_domain_30_days', URLTop10Domain30Days, dict(db=db,
                                                                    cursor_parser=cursor_parser,
                                                                    logger=logger)),
        (r'^/url_info', URLGetURLInfo, dict(db=db,
                                            cursor_parser=cursor_parser,
                                            logger=logger))
    ], **settings)
