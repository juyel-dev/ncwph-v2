from pydantic import BaseModel
from typing import List

class NCWPHConfig:
    IMAGE_SIZE = (256, 256)
    FEATURE_DIM = 512
    HASH_BITS = 256
    BASE_THRESHOLD = 42
    THRESHOLD_RANGE = (35, 58)
