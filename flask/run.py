def run_by_flask(app):
    from utils import watch_files_for_develop
    app.run(HOST, PORT, debug=True, extra_files=watch_files_for_develop(app))


def run_by_tornado(app):
    from tornado.httpserver import HTTPServer
    from tornado.wsgi import WSGIContainer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(PORT, address=HOST)
    IOLoop.instance().start()


def run_by_gevent(app):
    from gevent.pywsgi import WSGIServer

    http_server = WSGIServer((HOST, PORT), app)
    http_server.serve_forever()


HOST = '0.0.0.0'
PORT = 8899
TYPE = ''


def main(project: str):
    from sys import stderr

    if project == 'basic':
        from basic.app import app
    elif project == 'blueprint':
        from basic.app import app
    elif project == 'conf':
        from conf.app import app
    elif project == 'context_hook':
        from context_hook.app import app
    elif project == 'db':
        from db.app import app
    elif project == 'error_handler':
        from error_handler.app import app
    elif project == 'i18n':
        from i18n.app import app
    elif project == 'jinja':
        from jinja.app import app
    elif project == 'request':
        from request.app import app
    else:
        print('Invalid project name', file=stderr)
        return

    if TYPE == 'tornado':
        run_by_tornado(app)
    elif TYPE == 'gevent':
        run_by_gevent(app)
    else:
        run_by_flask(app)


if __name__ == '__main__':
    main('jinja')
