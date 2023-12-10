from fastapi import FastAPI

description = """
## Basic of FastAPI

This demo show how to use FastAPI simply, include:

- Basic Route
- Request and response
- Request arguments and validate
- Data model
"""

app = FastAPI(
    title="Basic of FastAPI",
    description=description,
    version="1.0.0",
    docs_url="/docs",
)


if __name__ == "__main__":
    import uvicorn

    # 启动服务器
    uvicorn.run("app:app", host="0.0.0.0", port=5001, log_level="info", reload=True)
