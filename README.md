```
Video transfer server and object tracking client
====================================

This repo illustrates sever sending a video of a bouncing ball to client and client responding with the predicted location of the moving ball using OpenCV.

Running
-------
First ensure the correct Python version (python3.10):

.. code-block:: console

    $ python -V

Second install the required packages:

.. code-block:: console

    $ pip install -r requirements.txt

To send offer to client:

.. code-block:: console

    $ python3 server.py

Once the offer signal from server is established, run client.py to process the video:

.. code-block:: console

    $ python3 client.py

The client will display the frames of the green moving ball with the red contour enclosing the object. The server will receive answer containing the predicted location of the ball from client, and compute the percentage error of the predicted and true values.

Makefile
------------------
Simply Docker and Kubernetes commands 

.. code-block:: console

    $ make build-client-image




Credits
-------
Template: https://github.com/aiortc/aiortc/blob/main/examples/server/README.rst
```
