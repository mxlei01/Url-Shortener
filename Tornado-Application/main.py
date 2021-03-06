import tornado
import tornado.ioloop
import tornado.web
import url_server.router.router_settings as settings
from url_server.router.router import create_application
from logger.logger import logger as logger

# main.py is the main access point of the tornado app, to run the application, just run "python main.py"

# What this will do is listen to port in the settings.py file, and then we can access the app using
# http://localhost:settings.port on any browser, or using python requests library
if __name__ == "__main__":
    # Set the application to listen to port 8888
    application = create_application()
    application.listen(settings.port)

    # Get the current IOLoop
    currentIOLoop = tornado.ioloop.IOLoop.current()

    # Log the port that is listened
    logger.info("Started application on port:" + str(settings.port))

    # Start the IOLoop
    currentIOLoop.start()