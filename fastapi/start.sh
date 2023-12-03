#!/usr/bin/env bash

function show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -p, --port    Port to listen on"
    echo "  -h, --host    Host to listen on"
    echo "  -w, --worker  Number of workers to use"
    echo "  -r, --reload  Enable auto reloading"
    echo "  -h, --help    Show this help message"
    echo "Example:"
    echo "  $0 -p 8000 -h 0.0.0.0 -w 4 -r"
}


function main() {
    app='basic'
    port='8899'
    host='0.0.0.0'
    worker='4'
    reload=''

    while [ $# -gt 0 ]; do
        case $1 in
        -a | --app)
            app=$2
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
        -r | --reload)
            reload='--reload'
            ;;
        -h | --help)
            show_help
            return -1
            ;;
        esac

        shift
    done

    eval ".venv/bin/uvicorn --port=$port --host=$host --threads=$thread --threads=${thread} ${app}.app:flask_app"

}

main $*
