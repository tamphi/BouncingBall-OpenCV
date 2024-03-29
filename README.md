Video transfer server and object tracking client
================================================

This repo illustrates sever sending a video of a bouncing ball to client and client responding with the predicted location of the moving ball using OpenCV.

Running
-------

First ensure the correct Python version (python3.10):

```
$ python -V
```

Second install the required packages: 

```
$ pip install -r requirements.txt
```

To send offer to client:

```
$ python3 server.py
```

Once the offer signal from server is established, run client.py to process the video:

```
$ python3 client.py
```

The client will display the frames of the **green** moving ball with the **red** contour enclosing the object. The server will receive answer containing the predicted location of the ball from client, and compute the percentage error of the predicted and true values.

![1711709440605](image/README/1711709440605.png)

Unittest
--------

Check BallVideoStreamTrack() object attributes and localization results threshold:

test_media.py -- ensure ball radius, (x,y) coordinates, screen width and heights, etc are within constraints

test_localize.py -- ensure localization percentage error of video frame are less than 10%

To run test `pytest tests` or `pytest tests -W ignore::DeprecationWarning` to ignore deprecation warnings

Makefile
--------

Simply Docker and Kubernetes commands:

To build client image `$ make build-client-image`

To build server image `$ make build-server-image`

For more commands, please checkout the file

Credits
-------

Template: https://github.com/aiortc/aiortc/blob/main/examples/server/README.rst
