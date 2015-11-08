import momoko
import momoko_settings
import tornado.ioloop

# momoko_pool.py contains the momoko_db_connection which can connect to a postgres database

# This will create a momoko db connection using dsn, size, and ioloop
#   dsn    : a dsn string that contains a few parameters we need to setup in order to connect to
#            postgres,
#              dbname   = database name
#              user     = username
#              password = password
#              host     = hostname
#              port     = port number
#   size   : the minimum amount of connections for postgres
#   ioloop : the current ioloop instance
momoko_db_connection = momoko.Pool(dsn='dbname=%s user=%s password=%s host=%s port=%s'
                                       % (momoko_settings.dbname, momoko_settings.user,
                                          momoko_settings.password, momoko_settings.host,
                                          momoko_settings.port),
                                   size=momoko_settings.num_connections,
                                   ioloop=tornado.ioloop.IOLoop.current())

# Call connect to establish connection with the momoko pool
momoko_db_connection.connect()