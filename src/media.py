
import numpy as np

import cv2
from aiortc import VideoStreamTrack
from av import VideoFrame

#example: https://github.com/aiortc/aiortc/blob/main/examples/videostream-cli/cli.py

class BallVideoStreamTrack(VideoStreamTrack):
    """
    A video track that returns an animated ball.
    """
    def __init__(self):
        super().__init__()  # don't forget this!
        self.setattr()

        #start animation 
        self.frames = []
        for k in range(self.n_frame):
            #bounce the ball
            self.bounce()
            #create canvas
            self.background = np.zeros((self.height, self.width,3),dtype='uint8')
            #add frame
            self.frames.append(
                VideoFrame.from_ndarray(
                    cv2.circle(self.background,(self.x, self.y),self.radius,self.color,-1), format="bgr24"
                )
            )

    async def recv(self):
        """
        Receive the next :class:~av.video.frame.VideoFrame.
        BallVideoStreamTrack :class:VideoStreamTrack
        """
        pts, time_base = await self.next_timestamp()

        self.bounce()
        self.background = np.zeros((self.height, self.width, 3), np.uint8)
        frame = VideoFrame.from_ndarray(cv2.circle(self.background, (self.x, self.y), self.radius, self.color, -1), format="bgr24")

        frame.pts = pts
        frame.time_base = time_base
        return frame
    
    def setattr(self):
        """
        Set animation attributes: background color, height & width, ball radius & color, move speed
        """
        self.height, self.width = 600, 800

        # ball attr
        self.radius = 40
        self.color = (0, 255, 0) # bgr value

        #starting point
        self.x = np.random.randint(self.radius,self.width - self.radius)
        self.y = np.random.randint(self.radius,self.height - self.radius)
        # ball speed 
        self.dx = 4 # x-axis
        self.dy = 4 # y-axis
        
        #canvas
        self.background = np.zeros((self.height, self.width,3),np.uint8)
        self.n_frame = 30
        
    def bounce(self):
        """
        Bounce the ball along x and y direction
        """
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        if self.y >= self.height - self.radius:
            self.dy *= -1
        elif self.y <= self.radius:
            self.dy *= -1

        if self.x >= self.width - self.radius:
            self.dx *= -1
        elif self.x <= self.radius:
            self.dx *= -1
