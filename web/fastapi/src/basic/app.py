from typing import Annotated, Any, Dict

from fastapi import FastAPI, Path, Query, Response, status

app = FastAPI()

# 定义 Name 查询参数
QueryName = Query(
    title="Name",
    description="Name of person",
    min_length=2,
    max_length=20,
)

# 定义 Gender 查询参数
QueryGender = Query(
    title="Gender",
    description="Gender of person",
    pattern=r"^(M|F)$",
)


@app.get("/api/hello", status_code=200)
async def get_hello_by_args_in_query(
    response: Response,
    name: Annotated[str, QueryName],
    gender: Annotated[str, QueryGender] = "M",
) -> Dict[str, Any]:
    """根据查询参数执行 GET 请求

    Args:
        - `response` (`Response`): 响应对象
        - `name` (`Annotated[str, QueryName]`): Name 请求参数
        - `gender` (`Annotated[str, QueryGender]`, optional): Gender 请求参数. Defaults to "M".

    Returns:
        `Dict[str, Any]`: 响应的 JSON 数据
    """
    name = name.strip()

    if not name:
        # 如果 name 参数无效, 则修改响应码为 400
        response.status_code = status.HTTP_400_BAD_REQUEST

        # 返回错误响应 JSON
        return {
            "status": "error",
            "payload": {"message": "Name is required"},
        }

    # 根据 gender 参数生成 title 值
    title = "Mr" if gender == "M" else "Ms"

    # 返回 JSON 数据
    return {
        "status": "success",
        "payload": {"message": f"Hello {title}. {name}"},
    }


# 定义 Name 路径参数
PathName = Path(
    title="Name",
    description="Name of person",
    min_length=2,
    max_length=20,
)


@app.get("/api/hello/{name}", status_code=200)
async def get_hello_by_args_in_path(
    response: Response,
    name: Annotated[str, PathName],
    gender: Annotated[str, QueryGender] = "M",
) -> Dict[str, Any]:
    """根据路径参数执行 GET 请求

    Args:
        - `response` (`Response`): 响应对象
        - `name` (`Annotated[str, QueryName]`): Name 路径参数
        - `gender` (`Annotated[str, QueryGender]`, optional): Gender 请求参数. Defaults to "M".

    Returns:
        `Dict[str, Any]`: 响应的 JSON 数据
    """
    name = name.strip()

    if not name:
        # 如果 name 参数无效, 则修改响应码为 400
        response.status_code = status.HTTP_400_BAD_REQUEST

        # 返回错误响应 JSON
        return {
            "status": "error",
            "payload": {"message": "Name is required"},
        }

    # 根据 gender 参数生成 title 值
    title = "Mr" if gender == "M" else "Ms"

    # 返回 JSON 数据
    return {
        "status": "success",
        "payload": {"message": f"Hello {title}. {name}"},
    }


if __name__ == "__main__":
    import uvicorn

    # 启动服务器
    uvicorn.run("app:app", host="0.0.0.0", port=5001, log_level="info", reload=True)
