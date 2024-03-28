import numpy as np
import cv2 as cv
from src.localize import *

async def display_and_queue_images(track, queue):
    """
    Using OpenCV to display received images and add frame to client processing queue

    Keyword arguments:
    track: received media track
    queue: multiprocessing queue
    """
    frame = None

    while True:
        media = await track.recv()
        frame = media.to_ndarray(format="bgr24")
        # queue.put(media)

        #plot contour
        center, radius = find_contour(frame)
        x = int(center[0])
        y = int(center[1])
        r = int(radius)
        cv.circle(frame, (x,y), r, (0, 0, 255), 2)

        cv.imshow("image", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()
    