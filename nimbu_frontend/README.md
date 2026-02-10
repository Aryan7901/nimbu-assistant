# 🍋 Nimbu Frontend: The Command Editor

This is the graphical user interface (GUI) for **Nimbu**, built with **Flutter**. It provides a sleek, user-friendly way to manage your custom voice commands without manually editing JSON files.

The frontend acts as a visual editor for `~/.nimbu/commands.json`, allowing you to add, remove, and modify the tools your voice assistant can use.

---

## ✨ Features

* **Visual Command Management:** Add new voice triggers and shell commands through a clean UI.
* **Real-time Validation:** Ensures your "Action Nicknames" are formatted correctly and are meaningfull to improve accuracy (no spaces).
* **Dark Mode UI:** Designed with a modern, high-contrast dark theme.
* **Cross-Platform Desktop Support:** Runs natively on Linux, Windows, and macOS.
* **Auto-Sync:** Changes saved here are instantly picked up by the running Python voice assistant (via the backend's file watcher).

---

## 🛠️ Prerequisites

To run or build this frontend, you need the **Flutter SDK** installed on your machine.

1.  **Install Flutter:** [Follow the official guide here](https://docs.flutter.dev/get-started/install).
2.  **Verify Installation:**
    ```bash
    flutter doctor
    ```
3.  **Enable Desktop Support (if not already enabled):**
    ```bash
    # For Linux
    flutter config --enable-linux-desktop

    # For Windows
    flutter config --enable-windows-desktop

    # For macOS
    flutter config --enable-macos-desktop
    ```

---

## 🚀 Getting Started

### 1. Installation

Navigate to the frontend directory inside the main repository:

```bash

# 1. Clone the repository if you have not cloned it yet
git clone https://github.com/Aryan7901/nimbu-assistant.git

cd nimbu-assistant/nimbu_frontend

# Install the dependencies
flutter pub get

# Run the app in dev mode
flutter run
```

## 🎮 How to Use

1.  **Open the App**: You will see a list of your current custom commands.
2.  **Add a New Command**:
    * Click the **"+ NEW COMMAND"** button at the bottom right.
    * **Action Nickname**: A unique ID for the tool, should be meaninful for better prompt detection (e.g., `launch_chrome`). Short name; no spaces allowed.
    * **What does this do?**: A natural language description (e.g., *"Opens the Google Chrome browser"*). This is the "prompt" the AI uses to understand your intent.
    * **Computer Command**: The actual shell command to run (e.g., `google-chrome` or `code .`).
3.  **Save**: Once you hit save (or close the editor), the app writes the changes to `~/.nimbu/commands.json`.
4.  **Voice Activation**: If the **Nimbu Python backend** is running, it will detect the file change via the watchdog and reload immediately. You can use your new command right away!

## 📦 Building for Release

To create a standalone executable for your operating system, run the appropriate command from within the `nimbu_frontend` directory:

```bash
# For Linux
flutter build linux

# For Windows
flutter build windows

# For macOS
flutter build macos
```
