import gc
from func_agent import FunctionAgent
from wake_word_detector import WakeWordDetector
import numpy as np
from faster_whisper import WhisperModel
import sounddevice as sd
import os

WAKE_WORD_GAIN = float(os.getenv("WAKE_WORD_GAIN",1.0))
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE",16000))
RECORDING_DURATION = float(os.getenv("RECORDING_DURATION",3.5))
WAKE_WORD_BLOCKSIZE = int(os.getenv("WAKE_WORD_BLOCKSIZE",1280))
WHISPER_MODEL = os.getenv("WHISPER_MODEL","base.en")


def play_ping_sound():
    """Play a simple beep to acknowledge wake word detection"""
    try:
        fs = 16000
        duration = 0.2
        frequency = 440
        
        t = np.linspace(0, duration, int(fs * duration))
        beep = np.sin(2 * np.pi * frequency * t) * 0.3
        
        sd.play(beep, fs)
        sd.wait()
    except Exception as e:
        print(f"Could not play ping: {e}")


class SpeechToText:
    def __init__(self):
        print(f"Loading Whisper model ({WHISPER_MODEL})...")
        self.model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        print("✓ Whisper ready")
    
    def transcribe(self, audio_data):
        segments, _ = self.model.transcribe(
            audio_data, 
            beam_size=5, 
            vad_filter=True, 
            temperature=0,
            vad_parameters=dict(min_silence_duration_ms=300),
            language="en",
        )
        return " ".join([segment.text for segment in segments])
    
class VoiceAssistantDaemon:
    def __init__(self,config,model,wv_model_dir, wake_word="hey_mycroft", threshold=0.5):
        print("=" * 60)
        print("🤖 VOICE ASSISTANT DAEMON INITIALIZING")
        print("=" * 60)
        self.wv_model_dir=wv_model_dir
        self.wake_word_detector = WakeWordDetector(wv_model_dir,wake_word, threshold,WAKE_WORD_GAIN)
        self.stt = SpeechToText()
        self.agent = FunctionAgent(config,model)
        self.wake_word=wake_word
        self.threshold=threshold
        self.fs = SAMPLE_RATE
        self.recording_duration = RECORDING_DURATION  # seconds
        self.listening_for_wake = True
        print("\n✅ All systems ready!")
        print(f"🎤 Say '{wake_word}' to activate")
        print("=" * 60)
    
    def capture_command(self):
        """Record audio for the specified duration"""
        print(f"\n🎤 Listening for command ({self.recording_duration}s)...")
        recording = sd.rec(
            int(self.recording_duration * self.fs), 
            samplerate=self.fs, 
            channels=1, 
            dtype='float32'
        )
        sd.wait()
        
        audio = recording.flatten()
        
        # Check if audio is too quiet
        if np.max(np.abs(audio)) < 0.02:
            print("⚠️  Audio too quiet, skipping...")
            return None
        
        return audio
    
    def wake_word_callback(self, indata, frames, time, status):
        """Callback for continuous wake word detection"""
        if not self.listening_for_wake:
            return
            
        if self.wake_word_detector.detect(indata.flatten()):
            self.listening_for_wake = False
            self.wake_detected = True
        
    def run(self):
        """Main daemon loop"""
        print("\n🟢 DAEMON RUNNING - Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Reset state
                self.listening_for_wake = True
                self.wake_detected = False
                
                # Listen for wake word
                stream = sd.InputStream(
                    samplerate=SAMPLE_RATE, 
                    blocksize=WAKE_WORD_BLOCKSIZE, 
                    channels=1, 
                    dtype='float32', 
                    callback=self.wake_word_callback
                )
                
                with stream:
                    while not self.wake_detected:
                        sd.sleep(100)
                
                # Stream is now closed, wake word detected!
                # Small delay to ensure stream is fully closed
                sd.sleep(200)
                
                play_ping_sound()
                
                audio = self.capture_command()
                
                if audio is not None:
                    text = self.stt.transcribe(audio)
                    
                    if text.strip():
                        print(f"📝 Transcribed: {text}")
                        
                        self.agent.execute(text)
                    else:
                        print("⚠️  No speech detected")
                
                print("\n⏳ Resetting... ")
                self.listening_for_wake=True
                self.wake_detected=False
                del self.wake_word_detector
                gc.collect()
                self.wake_word_detector=WakeWordDetector(self.wv_model_dir,self.wake_word,self.threshold,WAKE_WORD_GAIN)
                
                print("\n" + "=" * 60)
                print(f"🎤 Ready - Say '{self.wake_word_detector.wake_word}' again")
                print("=" * 60 + "\n")
                
        except KeyboardInterrupt:
            print("\n\n🛑 Daemon stopped by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
