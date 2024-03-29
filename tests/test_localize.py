import unittest
import sys
import cv2 as cv
import numpy as np
from src.localize import find_contour

class TestLocalize(unittest.TestCase):
    def setUp(self) -> None:
        self.radius = 40
        self.color = (0, 255, 0)
        self.height = 600
        self.width = 800
        self.x = np.random.randint(self.radius, self.width - self.radius)
        self.y = np.random.randint(self.radius, self.height - self.radius)
        self.background = np.zeros((self.height, self.width,3), dtype='uint8')
        self.cv_frame = cv.circle(self.background, (self.x, self.y), self.radius, self.color, -1)
        return super().setUp()
    
    def tearDown(cls) -> None:
        return super().tearDown()

    def test_find_contour_center(self):
        center, _ = find_contour(self.cv_frame)
        percentage_error_x = float(abs(center[0] - self.x)/self.x)*100.0
        percentage_error_y = float(abs(center[1] - self.y)/self.y)*100.0
        self.assertLessEqual((percentage_error_x,percentage_error_y),(10.0,10.0), f"(x,y) percentage error ({percentage_error_x}, {percentage_error_y})")

    def test_find_contour_radius(self):
        _ , r = find_contour(self.cv_frame)
        percentage_error_r = float(abs(r- self.radius)/self.radius)*100.0
        self.assertLessEqual(percentage_error_r, 10.0, f"radius percentage error {percentage_error_r}")

    


        

if __name__ == '__main__':
    unittest.main()