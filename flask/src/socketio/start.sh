#!/usr/bin/env bash

# gunicorn -w 4 -k gevent -b 0.0.0.0:8899 --log-level=debug -c app.py app:app

function main() {
    wsgi='gunicorn'
    port='8899'
    host='0.0.0.0'
    worker='4'
    thread='50'

    while [ $# -gt 0 ]; do
        case $1 in
        -w | --wsgi)
            wsgi=$2
            shift
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
        esac

        shift
    done

    if [ "$wsgi" == 'gunicorn' ]; then
        eval "../../.venv/bin/gunicorn -w $worker --threads $thread -k gevent -b $host:$port --log-level=debug app:app"
    elif [ "$wsgi" == 'uwsgi' ]; then
        eval "../../.venv/bin/uwsgi --http $host:$port --http-websockets --gevent 1000 --master --processes $worker --threads $thread --wsgi-file app.py --callable app"
    fi
}

main $*
