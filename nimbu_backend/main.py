import numpy as np
import ollama
import openwakeword.utils
import os
import json

from voice_assistant import VoiceAssistantDaemon

WAKE_WORD = "hey_mycroft"
THRESHOLD = 0.3
OLLAMA_MODEL = "qwen3:1.7b"



# Download model if it does not exist

base_dir = os.path.expanduser("~/.nimbu")
model_dir = os.path.join(base_dir, "models")
commands_file=os.path.join(base_dir,"commands.json")
os.makedirs(model_dir, exist_ok=True)

config={}
try:
    with open(os.path.join(base_dir,"commands.json")) as f:
        config=json.load(f)
except:
    data = {"custom_commands": []}
    with open(commands_file, "w") as f:
        json.dump(data, f, indent=4)
    config=data

# 2. Download to the specific target directory
openwakeword.utils.download_models(
    model_names=["hey_mycroft"],
    target_directory=model_dir
)

# Add this function after the imports and before the WAKE_WORD constants

def ensure_ollama_model(model_name: str):
    """Check if Ollama model exists, pull it if not."""
    try:
        models = ollama.list()
        model_names = [model['model'] for model in models.get('models', [])]
        
        model_exists = any(
            model_name in name or name.startswith(model_name + ':')
            for name in model_names
        )
        
        if not model_exists:
            print(f"📥 Pulling Ollama model '{model_name}'...")
            ollama.pull(model_name)
            print(f"✅ Model '{model_name}' downloaded")
        
    except Exception as e:
        print(f"❌ Error with Ollama: {e}")
        exit(1)

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigReloadHandler(FileSystemEventHandler):
    def __init__(self, daemon_container):
        self.daemon_container = daemon_container
        
    def on_modified(self, event):
        if event.src_path == commands_file:
            print("\n🔄 Config file changed! Reloading...")
            global config
            try:
                with open(commands_file) as f:
                    config = json.load(f)
                print(config)
                print("✅ Config reloaded successfully")
                
                # Reinitialize the daemon
                daemon:VoiceAssistantDaemon=self.daemon_container["daemon"]
                print("🔄 Reinitializing daemon...")
                daemon.agent.__init__(config)
                print("✅ Daemon reinitialized with new config")
            except Exception as e:
                print(f"❌ Error reloading config: {e}")

if __name__ == "__main__":
    ensure_ollama_model(OLLAMA_MODEL)
    daemon_container = {}
    daemon_container['daemon'] = VoiceAssistantDaemon(config=config,wake_word=WAKE_WORD, threshold=THRESHOLD)
    
    event_handler = ConfigReloadHandler(daemon_container)
    observer = Observer()
    observer.schedule(event_handler, path=base_dir, recursive=False)
    observer.start()
    
    try:
        daemon_container['daemon'].run()
    finally:
        observer.stop()
        observer.join()