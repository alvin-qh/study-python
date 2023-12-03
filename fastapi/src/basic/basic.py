from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/api/hello")
async def get_hello() -> Dict[str, Any]:
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
