#!/usr/bin/env python
#coding: utf-8

import os
from urllib2 import unquote

from tornado import web
from tornado import httpserver
from tornado import ioloop
from tornado import options

options.define('port', default=8888, type=int)


class Application(web.Application):
    def __init__(self, handlers=[], **kwargs):

        settings = dict({
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            "debug": True,
        }, **kwargs)

        handlers.extend([
            (r"/", static_router('index.html')),
            (r"/([^/]*)/", Book_index),
            (r"/(.*)", Book_content),
        ])

        super(Application, self).__init__(handlers, **settings)


def static_router(filename):
    '''route url to file.'''
    class Static(web.RequestHandler):
        def get(self):
            self.render(filename)
    return Static


class Book_index(web.RequestHandler):
    '''access book_xx/index.html, set url like http://.../book_xx/'''
    def get(self, name):
        self.render('%s/index.html'%unquote(name).encode('utf-8'))


class Book_content(web.StaticFileHandler):
    '''handler url like /book_name/....'''
    def __init__(self, application, request, **kwargs):
        kwargs['path'] = os.path.join(os.path.dirname(__file__), '.')
        super(Book_content, self).__init__(application, request, **kwargs)


if __name__ == '__main__':
    import logging
    options.parse_command_line()

    app = Application()
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)

    logging.info('run on %d'%options.options.port)
    ioloop.IOLoop.instance().start()
