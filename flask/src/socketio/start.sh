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

    # if [ wsgi = 'gunicorn' ]; then
    #     echo "gunicorn"
    # fi
    echo "$wsgi, $port, $host, $worker, $thread"
}

main $*
