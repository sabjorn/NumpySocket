# NumpySocket
## About
This python module is designed to send/receive Numpy arrays (compressed) over a TCP/IP socket. It was originally written to stream video frames from OpenCV however any Numpy array should work.

The original purpose of this module is to send video frames (captured with OpenCV) from a headless Raspberry PI to another computer.

## Topology
Currently, this library only allows for a `one-to-one` single connection setup (one client, one server). The relationship is not dynamic since a client cannot disconnect from the server and then have another client make a new connection. 

## Getting Started
The `server` needs to be started first. Once started it will wait for a `client` connection. Once the `client` is connected the `server` and `client` can each send and receive data.

### Example
In two separate terminal instances navigate to `./exmples/Simple`

In terminal 1, run:
```
python3 simple_server.py 
```

In terminal 2, run:
```
python3 simple_client.py
```

You should see a message arrive to the `server` window from the `client`.

## Development Goals
### Features
* alternatate topologies: `one-to-many` and `many-to-many`
* proper "server": allowing multiple clients to connect, disconnect, and re-connect
* `asyncio` support: this will either be a built in feature or a layer on top allowing for server and client to be run as asyncronous processes. 