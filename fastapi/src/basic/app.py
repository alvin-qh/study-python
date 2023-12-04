from typing import Any, Dict, Tuple

from fastapi import FastAPI, HTTPException, status

app = FastAPI()


@app.get("/api/hello")
async def get_hello() -> Dict[str, Any]:
    return {
        "status": "success",
        "payload": {"message": "Hello World"},
    }


@app.get("/api/hello/{name}")
async def get_hello_name(name: str) -> Tuple[Dict[str, Any], int] | Dict[str, Any]:
    name = name.strip()

    if not name:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {
                "status": "error",
                "payload": {"message": "Name is required"},
            },
        )

    return {
        "status": "success",
        "payload": {"message": f"Hello {name}"},
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=5001, log_level="info", reload=True)
