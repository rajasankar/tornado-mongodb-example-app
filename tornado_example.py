from pymongo.mongo_client import MongoClient
from tornado import web, httpserver
from tornado.options import define, options, parse_command_line
import json
import logging
import os
import tornado.autoreload
import traceback

define( "port", default = 8888, type = int )
class Example( tornado.web.Application ):
    def __init__( self ):
        handlers = [
                    ( r"/", HomeHandler ),
                    ( r"/api", MyAPIHandler ),
                    ( r"/demo", DemoUI )
                    ]
        settings = dict( 
                            template_path = os.path.join( '/home/test/website/', "templates" ),
                            static_path = os.path.join( '/home/test/website/', 'assets' )
                            xsrf_cookies = True,
                         )
        super( Example, self ).__init__( handlers, **settings )
        session = MongoClient()
        self.firstCol = session.firstDB.firstCol
        self.secondCol = session.secondDB.secondCol
class BaseHandler( tornado.web.RequestHandler ):
    @property
    def secondCol( self ):
        return self.application.secondCol
    @property
    def firstCol( self ):
        return self.application.firstCol
class DemoUI( BaseHandler )
    def get( self ):
	number= [i for i in range(0,10) ]
    self.render( "two.html" , title = "one",numberlist=number )
class HomeHandler( BaseHandler ):
    def get( self ):
        self.render( "index.html" )
class MyAPIHandler( BaseHandler ):
    def check_xsrf_cookie( self ):
        pass
    @tornado.web.asynchronous
    def get( self ):
        self.finish( "Please use POST for API" )
    @tornado.web.asynchronous
    def post( self ):
      value = secondCol.find_one({})
      self.finish( "Return from DB "+value  )
def main():
    options.logging = None
    access = logging.NullHandler()
    access.setLevel( logging.DEBUG )
    logging.getLogger( "tornado.access" ).addHandler( access )
    logging.getLogger( "tornado.access" ).propagate = False
    LOG_FILENAME = '/home/test/logging.log'
    handler = logging.handlers.RotatingFileHandler( LOG_FILENAME, maxBytes = 1 * 1024 * 1024, backupCount = 10 )
    formatter = logging.Formatter( 
        '%(asctime)s process [%(process)d]: %(message)s',
        '%b %d %H:%M:%S' )
    handler.setFormatter( formatter )
    logger = logging.getLogger()
    logger.addHandler( handler )
    logger.setLevel( logging.DEBUG )
    tornado.autoreload.start()
    parse_command_line()
    http_sever = tornado.httpserver.HTTPServer( Example() )
    http_sever.listen( options.port )
    tornado.ioloop.IOLoop.current().start()

try:
    main()
except:
    print traceback.format_exc()