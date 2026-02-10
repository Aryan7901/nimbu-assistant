import os
from openwakeword.model import Model
import numpy as np

class WakeWordDetector:
    def __init__(self,model_dir, wake_word: str = "hey_mycroft", threshold: float = 0.5,gain:float=1.0,):
        print(f"Initializing OpenWakeWord for: {wake_word}...")
        self.gain=gain
        model_path = os.path.join(model_dir, f"{wake_word}_v0.1.onnx")
        self.model = Model(
            wakeword_models=[model_path], 
            inference_framework='onnx'
        )
        
        self.wake_word = wake_word
        self.threshold = threshold
        print(f"✓ Detector ready. Threshold: {self.threshold}")
    
    def detect(self, audio_chunk: np.ndarray) -> bool:

        if audio_chunk.dtype == np.float32:
            audio_int16 = np.clip(audio_chunk * 32767 * self.gain, -32768, 32767).astype(np.int16)
        else:
            audio_int16 = np.clip(audio_chunk * self.gain, -32768, 32767).astype(np.int16)

        prediction = self.model.predict(audio_int16)
        score = prediction.get(f"{self.wake_word}_v0.1", 0.0)
        if score > self.threshold: 
            print(f"🎯 Wake word detected! Score: {score:.2f}")
            return True

        return False

