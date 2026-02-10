# 🍋 Nimbu: Local AI Voice Assistant

**Nimbu** is a privacy-first, fully local voice assistant. No cloud APIs, no data mining—just your voice, your hardware, and a local LLM. It integrates **OpenWakeWord** for detection, **Faster-Whisper** for transcription, and **Ollama** for function calling.

---

## 🏗️ System Architecture

Nimbu operates in a continuous loop: monitoring for a wake word, transcribing your intent, and executing the corresponding system function.



1.  **Wake Word Detector:** Uses `openwakeword` to constantly monitor audio for "Hey Mycroft."
2.  **Speech-to-Text (STT):** Once triggered, `faster-whisper` converts your spoken command into text.
3.  **Function Agent:** The LLM (via `Ollama`) parses the text to see if it matches built-in tools or custom commands.
4.  **Execution:** The system adjusts hardware (volume/brightness) or runs a shell script defined in your config.

---

## ✨ Key Features

* **100% Local:** Everything runs on your hardware (CPU/GPU). No internet required after setup.
* **Natural Language Intelligence:** Understands context. "It's too loud" or "Mute the sound" both trigger the volume tool correctly.
* **Hot-Reloading Config:** Modify `~/.nimbu/commands.json` and the assistant reloads your new commands instantly without a restart.
* **Cross-Platform:** Native support for Windows, macOS, and Linux hardware controls. Although testing has been primarily done on Linux. Feel free to raise an issue if you encounter issues on your OS.

---

## 🚀 Getting Started

### 1. Prerequisites
* **Python 3.11**
* **Ollama:** [Install here](https://ollama.com/).
* **System Dependencies (Linux only - Can skip if default commands are not required):**
    ```
    libasound2-dev brightnessctl ffmpeg
    ```

### 2. Installation
```bash
# 1. Clone the repository
git clone https://github.com/Aryan7901/nimbu-assistant.git
cd nimbu-assistant/nimbu_backend

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
# Windows only: pip install pycaw comtypes
## 🚀 Running the Assistant
```
Follow these steps to get **Nimbu** up and running on your machine:

1.  **Ensure Ollama is active:**
    The Ollama backend must be running for function calling to work.

    ```bash
    ollama serve
    ```

2.  **Start the Daemon:**
    Run the main script from your terminal. It will automatically check for models and create necessary directories.

    ```bash
    python main.py
    ```

3.  **Voice Interaction:**
    - Say **"Hey Mycroft"** (or your configured wake word).
    - Wait for the **beep (ping)** sound.
    - Give a command like: _"Set the volume to 50%"_ or _"Open github.com"_.

---

## ⚙️ Configuration & Customization

### Environment Variables

You can tweak performance and behavior using environment variables:

| Variable         | Default       | Description                                                                            |
| :--------------- | :------------ | :------------------------------------------------------------------------------------- |
| `WAKE_WORD`      | `hey_mycroft` | Phrase used to activate the listener. (options: `alexa`, `hey_mycroft`, `hey_jarvis` ) |
| `THRESHOLD`      | `0.3`         | Sensitivity of the wake word (0.0 to 1.0).                                             |
| `OLLAMA_MODEL`   | `qwen3:1.7b`  | The specific Ollama model to be used.                                                  |
| `WHISPER_MODEL`  | `base.en`     | Transcription model (`tiny.en`, `base.en`, etc.).                                      |
| `WAKE_WORD_GAIN` | `1.0`         | Digital gain for the microphone input.                                                 |

### Custom Commands (`commands.json`)

Nimbu creates a config folder at `~/.nimbu/`. The assistant monitors `commands.json` for changes in real-time. You can also use the GUI to edit the commands.json file.

**Example `commands.json`:**

```json
{
  "custom_commands": [
    {
      "name": "open_code",
      "description": "Opens Visual Studio Code/VS Code.",
      "command": "code"
    },
    {
      "name": "pause_video_audio",
      "description": "Pause the audio/video playing.",
      "command": "playerctl pause"
    }
  ]
}
```
