import socketio

sio = socketio.Client(

)


@sio.event
def connect():
    print("connection established")


@sio.event
def my_message(data):
    print("message received with ", data)
    sio.emit("my response", {"response": "my response"})


@sio.event
def disconnect():
    print("disconnected from server")


sio.connect(
    url="http://localhost:5600",
    socketio_path="_sio",
)
sio.wait()
