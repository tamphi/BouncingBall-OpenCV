import numpy as np
import cv2 as cv

async def display_and_queue_images(track, queue):
    """
    Using OpenCV to display received images and add frame to client processing queue

    Keyword arguments:
    track: received media track
    queue: multiprocessing queue
    """
    frame = None

    while True:
        frame = await track.recv()
        media = frame.to_ndarray(format="bgr24")
        # queue.put(media)
        cv.imshow("image", media)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()
    