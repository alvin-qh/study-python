#!/usr/bin/env bash

all_wsgi=(
    "gunicorn"
    "uwsgi"
    "waitress"
)

function show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"

    IFS=$', ';
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
    wsgi='gunicorn'
    port='8899'
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
        esac

        shift
    done

    if [ "$wsgi" == 'gunicorn' ]; then
        eval ".venv/bin/gunicorn -w $worker --threads $thread -k gevent -b $host:$port --log-level=DEBUG ${app}.app:flask_app"
    elif [ "$wsgi" == 'uwsgi' ]; then
        eval ".venv/bin/uwsgi --http $host:$port --http-websockets --master --processes $worker --threads $thread -w ${app}.app:flask_app"
    elif [ "$wsgi" == 'waitress' ]; then
        eval ".venv/bin/waitress-serve --port=$port --host=$host --threads=$thread --threads=${thread} ${app}.app:flask_app"
    fi
}

main $*
