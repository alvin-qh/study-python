#!/usr/bin/env bash

all_wsgi=(
    "gunicorn"
    "uwsgi"
    "waitress"
)

function show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -a, --app     Application to run"

    IFS=$', '
    echo "  -w, --wsgi    WSGI server to use ${all_wsgi[*]}"
    IFS=$''

    echo "  -p, --port    Port to listen on"
    echo "  -h, --host    Host to listen on"
    echo "  -w, --worker  Number of workers to use"
    echo "  -t, --thread  Number of threads per worker"
    echo "  -h, --help    Show this help message"
    echo "Example:"
    echo "  $0 -w uwsgi -p 8000 -h 0.0.0.0 -w 4 -t 50"
}


function main() {
    app='basic'
    wsgi='waitress'
    port='5001'
    host='0.0.0.0'
    worker='4'
    thread='50'

    while [ $# -gt 0 ]; do
        case $1 in
        -a | --app)
            app=$2
            shift
            ;;
        -w | --wsgi)
            wsgi=$2
            shift

            if ! [[ "${all_wsgi[*]}" =~ "$wsgi" ]]; then
                echo
                echo "Invalid WSGI server: \"$wsgi\""
                echo
                show_help
                return -1
            fi
            ;;
        -p | --port)
            port=$2
            shift
            ;;
        -h | --host)
            host=$2
            shift
            ;;
        -w | --worker)
            worker=$2
            shift
            ;;
        -t | --thread)
            thread=$2
            shift
            ;;
        -h | --help)
            show_help
            return -1
            ;;
        *)
            show_help
            return -1
        esac

        shift
    done

    if [ "$app" == 'quart_' ]; then
        # 对于 Quart 框架, 无法使用 WSGI 服务器启动, 而需要 ASGI 服务器来启动
        # https://pgjones.gitlab.io/hypercorn/tutorials/quickstart.html
        eval ".venv/bin/hypercorn --bind $host:$port --worker-class asyncio --workers $worker --access-logfile - --reload quart_.app:quart_app"
    else
        # 对于 Flask 框架, 可以使用 WSGI 服务器来启动
        if [ "$wsgi" == 'gunicorn' ]; then
            # https://gunicorn.org/#quickstart
            if [ "$app" == 'socketio_' ]; then
                # 如果通过 gunicorn 启动 websocket, 则 worker 数量必须为 1, 否则无法进行正常的负载均衡
                # 要解决这个问题, 可以在前面加上 Nginx 进行真正的负载均衡, 或者使用 uwsgi 服务器
                # https://flask-socketio.readthedocs.io/en/latest/deployment.html#gunicorn-web-server
                worker=1
                worker_class='geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
            else
                worker_class='gevent'
            fi
            eval ".venv/bin/gunicorn -w $worker --threads $thread -k $worker_class -b $host:$port --log-level=DEBUG ${app}.app:flask_app"
        elif [ "$wsgi" == 'uwsgi' ]; then
            # https://uwsgi-docs.readthedocs.io/en/latest/#quickstarts
            use_websocket=''
            if [ "$app" == 'socketio_' ]; then
                use_websocket='--http-websockets'
                worker=1
            else
                worker=4
            fi
            eval ".venv/bin/uwsgi --http $host:$port --gevent 1000 $use_websocket --master --workers $worker -w ${app}.app:flask_app"
        elif [ "$wsgi" == 'waitress' ]; then
            # https://docs.pylonsproject.org/projects/waitress/en/stable/usage.html
            eval ".venv/bin/waitress-serve --port $port --host $host --threads=$worker ${app}.app:flask_app"
        fi
    fi
}

main $*
