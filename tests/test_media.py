import unittest
import sys
sys.path.append("..")
from src.media import BallVideoStreamTrack

class TestMedia(unittest.TestCase):

    def setUp(self) -> None:
        self.ball = BallVideoStreamTrack()
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_radius_min_val(self):
        self.assertGreater(self.ball.radius, 0)
    
    def test_radius_max_val(self):
        diameter = int(self.ball.radius*2)
        self.assertLessEqual(diameter, min(self.ball.width,self.ball.height))

    def test_x_min_val(self):
        self.assertGreaterEqual(self.ball.x, self.ball.radius)

    def test_y_min_val(self):
        self.assertGreaterEqual(self.ball.y, self.ball.radius)
    
    def test_x_max_val(self):
        self.assertLessEqual(self.ball.x, self.ball.width - self.ball.radius)

    def test_y_max_val(self):
        self.assertLessEqual(self.ball.y, self.ball.height - self.ball.radius)

    def test_width_min_val(self):
        self.assertGreaterEqual(self.ball.width, 240)

    def test_height_min_val(self):
        self.assertGreaterEqual(self.ball.height, 240)
        

if __name__ == '__main__':
    unittest.main()