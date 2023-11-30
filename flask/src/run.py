import importlib
from typing import Literal, Union

from flask import Flask


def run_by_flask(app: Flask, host: str, port: int) -> None:
    from utils import get_watch_files_for_develop

    app.run(host, port, debug=True, extra_files=get_watch_files_for_develop(app))


def run_by_tornado(app: Flask, host: str, port: int) -> None:
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from tornado.wsgi import WSGIContainer

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port, address=host)
    IOLoop.instance().start()


def run_by_gevent(app: Flask, host: str, port: int) -> None:
    from gevent.pywsgi import WSGIServer

    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()


ServerType = Union[Literal["tornado"], Literal["gevent"], Literal["flask"]]


def main(
    app_name: str,
    server_type: ServerType = "flask",
    host: str = "0.0.0.0",
    port: int = 8899,
) -> None:
    m = importlib.import_module(app_name)
    app: Flask = m.app

    match server_type:
        case "flask":
            run_by_flask(app, host, port)
        case "tornado":
            run_by_tornado(app, host, port)
        case "gevent":
            run_by_tornado(app, host, port)
        case _:
            raise ValueError(f"Unknown server type: {server_type}")


if __name__ == "__main__":
    main("conf")
