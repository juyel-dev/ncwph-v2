import cv2
import numpy as np
from .config import NCWPHConfig

class Preprocessor:
    def process(self, image: np.ndarray) -> dict:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, NCWPHConfig.IMAGE_SIZE)
        gray = cv2.GaussianBlur(gray, (5, 5), 1.0)
        
        results = {
            'grayscale': gray,
            'quality_score': self._assess_quality(gray),
            'depth_map': self._estimate_depth(gray)
        }
        return results

    def _assess_quality(self, img):
        return cv2.Laplacian(img, cv2.CV_64F).var() / 500.0

    def _estimate_depth(self, img):
        # Simple phase congruency approximation
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        return np.sqrt(sobelx**2 + sobely**2)
