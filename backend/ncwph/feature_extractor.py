import numpy as np
import cv2
from skimage.feature import local_binary_pattern
from .config import NCWPHConfig

class FeatureExtractor:
    def extract(self, preprocessed: dict) -> np.ndarray:
        gray = preprocessed['grayscale']
        features = []
        
        # Zernike-like (simplified Hu + custom)
        moments = cv2.moments(gray)
        hu = cv2.HuMoments(moments).flatten()
        features.extend(hu)
        
        # LBP
        lbp = local_binary_pattern(gray, 8, 1, method='uniform')
        hist, _ = np.histogram(lbp.ravel(), bins=10, range=(0, 10))
        features.extend(hist)
        
        # SPP (Spatial Pyramid Pooling)
        h, w = gray.shape
        for level in [1, 2, 4]:
            step = h // level
            for i in range(level):
                for j in range(level):
                    cell = gray[i*step:(i+1)*step, j*step:(j+1)*step]
                    features.extend([np.mean(cell), np.std(cell)])
        
        vector = np.array(features, dtype=np.float32)
        # Pad to fixed size
        if len(vector) < NCWPHConfig.FEATURE_DIM:
            vector = np.pad(vector, (0, NCWPHConfig.FEATURE_DIM - len(vector)))
        else:
            vector = vector[:NCWPHConfig.FEATURE_DIM]
        
        return vector / (np.linalg.norm(vector) + 1e-8)
