import cv2 as cv
import numpy as np
import imutils
import argparse
import time
import asyncio
from concurrent.futures import ProcessPoolExecutor

#tutorial: https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

def find_contour(frame):
    """
    Find the contour of the ball and its center coordinates (x,y)

    Keyword arguments:
    frame: current video frame 
    """

    #define upper and lower hsv value for ball color
    lower_hsv = (29, 86, 6) #green
    upper_hsv = (64, 255, 255) #green

    ## optional: add blur filter
    # frame = cv.GaussianBlur(frame, (11, 11), 0)

    # convert frame to hsv and create mask 
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_hsv, upper_hsv)

    ## optional: dilations and erosion to remove small mask blobs
    # mask = cv.erode(mask, None, iterations=2)
    # mask = cv.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    #find the largest contour
    max_cnt = max(cnts, key=cv.contourArea)
    coordinates, radius = cv.minEnclosingCircle(max_cnt)

    return coordinates, radius

async def mp_find_contour(queue, mpX, mpY):
    """
    Multiprocess routine call to find and update ball position (x,y) for each frame in queue
    """
    while True:
        executor = ProcessPoolExecutor(max_workers=1)
        frame = queue.get(True) #blocking call
        center, _ = find_contour(frame)
        mpX.value = center[0]
        mpY.value = center[1]


def start_process_a(queue, mpX, mpY):
    """
    Start process to calculate ball position

    Keyword arguments:
    queue: queue to store frame
    mpX: x coordinate of ball as mp.Value
    mpY: y coordinate of ball as mp.Value
    """
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(mp_find_contour(queue, mpX, mpY))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
   

if __name__ == "__main__":
    """
    Test tracking algorithm
    """
    parser = argparse.ArgumentParser(description="Tracking ball")
    parser.add_argument("--video", default = "video.mp4", help ="Path to video")

    args =vars(parser.parse_args())

    #grab video
    vs = cv.VideoCapture(args["video"])
    time.sleep(2.0)

    # 10s video contaning 30 frames per second
    for k in range(300):
        frame = vs.read()
        # handle the frame from VideoCapture or VideoStream
        frame = frame[1] if args.get("video", False) else frame
        
        #plot contour
        center, radius = find_contour(frame)
        x = int(center[0])
        y = int(center[1])
        r = int(radius)
        cv.circle(frame, (x,y), r, (0, 0, 255), 2)
        cv.imshow("tracking", frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()
    pass