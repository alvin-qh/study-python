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
    port='5001'
    # host='[::]'
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
        *)
            show_help
            return -1
            ;;
        esac

        shift
    done

    # 使用 FastAPI 默认的 Uvicorn 服务器, 参考 https://www.uvicorn.org/settings 配置信息
    # eval ".venv/bin/uvicorn --port $port --host $host --workers $worker $reload $app.app:app --app-dir src"

    # 使用 Hypercorn 开启 HTTP/2, 支持 https, 参考 https://hypercorn.readthedocs.io/en/latest/how_to_guides/configuring.html 配置信息
    # eval ".venv/bin/hypercorn --keyfile cert/key.pem --certfile cert/cert.pem --bind $host:$port --workers $worker $reload $app.app:app --worker-class asyncio --root-path src"

    # 使用 Hypercorn 服务器, 参考 https://hypercorn.readthedocs.io/en/latest/how_to_guides/configuring.html 配置信息
    eval ".venv/bin/hypercorn --log-level DEBUG --bind $host:$port --workers $worker $reload $app.app:app --worker-class asyncio --root-path src"
}

main $*
