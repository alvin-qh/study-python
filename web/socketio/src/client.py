from typing import Any
import socketio

sio = socketio.Client()


@sio.event
def connect() -> None:
    print("connection established")


@sio.event
def my_message(data: Any) -> None:
    print("message received with ", data)
    sio.emit("my response", {"response": "my response"})


@sio.event
def disconnect() -> None:
    print("disconnected from server")


sio.connect(
    url="http://localhost:5600",
    socketio_path="_sio",
)
sio.wait()
