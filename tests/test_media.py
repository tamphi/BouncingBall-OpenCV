import unittest
import sys
sys.path.append("..")
from src.media import BallVideoStreamTrack

class TestMedia(unittest.TestCase):
    def test_radius_min_val(self):
        ball = BallVideoStreamTrack()
        self.assertGreater(ball.radius, 0)
    
    def test_radius_max_val(self):
        ball = BallVideoStreamTrack()
        diameter = int(ball.radius*2)
        self.assertLessEqual(diameter, min(ball.width,ball.height))

    def test_x_min_val(self):
        ball = BallVideoStreamTrack()
        self.assertGreaterEqual(ball.x, ball.radius)

    def test_y_min_val(self):
        ball = BallVideoStreamTrack()
        self.assertGreaterEqual(ball.y, ball.radius)
    
    def test_x_max_val(self):
        ball = BallVideoStreamTrack()
        self.assertLessEqual(ball.x, ball.width - ball.radius)

    def test_y_max_val(self):
        ball = BallVideoStreamTrack()
        self.assertLessEqual(ball.y, ball.height - ball.radius)

    def test_width_min_val(self):
        ball = BallVideoStreamTrack()
        self.assertGreaterEqual(ball.width, 240)

    def test_height_min_val(self):
        ball = BallVideoStreamTrack()
        self.assertGreaterEqual(ball.height, 240)
        

if __name__ == '__main__':
    unittest.main()