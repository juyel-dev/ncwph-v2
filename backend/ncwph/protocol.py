from .preprocessor import Preprocessor
from .feature_extractor import FeatureExtractor
from .hasher import AdvancedHasher

class NCWPHProtocol:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.extractor = FeatureExtractor()
        self.hasher = AdvancedHasher()
        self.enrollments = {}  # In-memory (use DB in prod)

    def enroll(self, image: np.ndarray, user_id: str):
        pre = self.preprocessor.process(image)
        features = self.extractor.extract(pre)
        hash_val = self.hasher.hash(features)
        
        self.enrollments[user_id] = {
            'hash': hash_val,
            'features': features.tolist(),
            'metadata': {'quality': pre['quality_score']}
        }
        return {"status": "enrolled", "hash": hash_val, "user_id": user_id}

    def verify(self, image: np.ndarray, user_id: str):
        if user_id not in self.enrollments:
            return {"match": False, "confidence": 0}
        
        pre = self.preprocessor.process(image)
        features = self.extractor.extract(pre)
        hash_val = self.hasher.hash(features)
        
        stored = self.enrollments[user_id]
        hamming = sum(a != b for a, b in zip(hash_val, stored['hash'])) 
        similarity = 1 - (hamming / len(hash_val))
        
        confidence = float(similarity)
        return {
            "match": confidence > 0.65,
            "confidence": confidence,
            "decision": "ACCEPT" if confidence > 0.85 else "CHALLENGE"
      }
