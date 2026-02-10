import platform
import subprocess
import webbrowser


def open_system_browser(url):
    if url and not url.startswith(('http://', 'https://', 'file://')):
        url = 'https://' + url
    try:
        webbrowser.open(url, new=2)
        return f"Opening {url} in default browser..."
    except Exception as e:
        return f"Error opening browser: {str(e)}"


def set_system_volume(level):
    level = max(0, min(100, int(level)))
    os_name = platform.system()

    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(["osascript", "-e", f"set volume output volume {level}"], check=True)
            return f"macOS volume set to {level}%"
        elif os_name == "Linux":
            subprocess.run(["amixer", "sset", "Master", f"{level}%"], check=True, stdout=subprocess.DEVNULL)
            return f"Linux volume set to {level}%"
        elif os_name == "Windows":
            from pycaw.pycaw import AudioUtilities

            volume = AudioUtilities.GetSpeakers().EndpointVolume
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)

            return f"Windows volume set to {level}%"
    except Exception as e:
        return f"Error setting volume: {str(e)}"


def set_system_brightness(level):
    level = max(0, min(100, int(level)))
    os_name = platform.system()

    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(["osascript", "-e", f"tell application \"System Events\" to set brightness of primary display to {level / 100.0}"], check=True)
            return f"macOS brightness set to {level}%"

        elif os_name == "Linux":
            subprocess.run(["brightnessctl", "set", f"{level}%"], check=True)
            return f"Linux brightness set to {level}%"

        elif os_name == "Windows":
            ps_command = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {level})"
            subprocess.run(["powershell", "-Command", ps_command], check=True)
            return f"Windows brightness set to {level}%"
        
        return f"Error: Unsupported OS '{os_name}'"
    except Exception as e:
        return f"Error setting brightness: {str(e)}"

