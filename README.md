# 🍋 Nimbu: Local AI Voice Assistant

**Nimbu** is a privacy-first, fully local voice assistant. No cloud APIs, no data mining—just your voice, your hardware, and a local LLM.

---

## 📂 Project Modules

This repository is a monorepo containing two distinct components:

| Module | Description | Path |
| :--- | :--- | :--- |
| **🧠 Backend** | The core voice daemon. Handles wake word detection (`OpenWakeWord`), transcription (`Faster-Whisper`), and intent recognition (`Ollama`). | [**Explore Backend**](./nimbu_backend/README.md) |
| **🖥️ Frontend** | A cross-platform GUI (Linux/Windows/macOS) built with Flutter. Use this to visually manage and add custom voice commands. | [**Explore Frontend**](./nimbu_frontend/README.md) |

---

## 🏗️ How It Works

Nimbu operates as a local system where the **Backend** runs in the background listening for commands, and the **Frontend** acts as the configuration dashboard.

1.  **The Backend** listens for the wake word *"Hey Mycroft"*.
2.  When triggered, it transcribes your speech and uses a local LLM (via Ollama) to determine the best action.
3.  **The Frontend** writes to a shared configuration file (`~/.nimbu/commands.json`).
4.  **Hot-Reloading:** When you save a new command in the Frontend app, the Backend detects the file change and updates its capabilities instantly—no restart required.

---

## 🚀 Quick Start

To get the full experience running, you will need to set up both components.

### 1. Clone the Repository
```bash
git clone https://github.com/Aryan7901/nimbu-assistant.git
cd nimbu-assistant
```

### 2. Setup Components

Please follow the detailed installation and running instructions provided in each module's README:

* **Backend Setup:** [Read nimbu_backend/README.md](./nimbu_backend/README.md)
* **Frontend Setup:** [Read nimbu_frontend/README.md](./nimbu_frontend/README.md)

**Note:** The frontend is completely optional. You can manage everything by editing the `commands.json` file manually if you prefer a CLI-only experience.
