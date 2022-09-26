# NumpySocket
## About
Provides a subclass of `socket.socket` that enables a TCP/IP socket that can send and recieve Numpy arrays with the same interface as a regular Python `socket`.

### Methods
The subclass of `socket.socket` provides three key method overrides. All other `socket` methods are untouched.

* `sendall` - takes a Numpy array as an argument to send an Array
* `recv` - outputs a Numpy array (`len() == 0` if no data received)

## Installation
### venv (optional)
Run:
```
python -m venv .venv
source .venv/bin/activate
```

### Install
From within this git repo, run:
```
pip install .
```

## Examples
There are two separate examples showing how to create a client and sever using a `NumpySocket`

### Simple
`./examples/Simple` shows a **server** which closes after the client disconnects.

In terminal 1, run:
```
python simple_server.py 
```

In terminal 2, run:
```
python simple_client.py
```

### OpenCV
`./examples/OpenCV` shows an actual usecase for this library (sending video frames). This example requires installing additional requirements (`./examples/openCV/requirements.txt`).

This example also shows how to create a persistent **server** which allows for new clients to connect after old clients disconnects.

In terminal 1, run:
```
python cv_server.py 
```

In terminal 2, run:
```
python cv_client.py
```

Kill terminal 2 and re-run the command and the **server** will allow for the new connection.
