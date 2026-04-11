# sript.py
# Requirements: pip install pyaudio numpy psutil
# Run once to install: python sript.py --install

import pyaudio
import numpy as np
import subprocess
import time
import sys
import os
import psutil
import random

# ── CONFIG ──────────────────────────────────────────────────────────────────
CLAP_THRESHOLD  = 3000
DOUBLE_CLAP_GAP = 0.6
COOLDOWN        = 3.0
CHUNK           = 1024
SAMPLE_RATE     = 44100
CHECK_INTERVAL  = 2.0

CLAUDE_PATH      = r"C:\Users\HP\AppData\Local\SquirrelTemp\tempb\lib\net45\claude.exe"
ANTIGRAVITY_PATH = r"C:\Users\HP\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Antigravity\Antigravity.lnk"
FLAG_FILE        = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".first_run_done")
# ────────────────────────────────────────────────────────────────────────────

CATCHY_LINES = [
    "Welcome back, Master. Your tools await.",
    "At your service, Master. Let us build.",
    "The clap has spoken. Opening your world.",
    "Good to see you again, Master.",
    "Ready when you are, Master.",
    "Your command has been received, Master.",
    "Firing up the engines, Master.",
    "Rise and grind, Master. Let us get to work.",
    "Back again? Let us make something great.",
    "Your workspace is being prepared, Master.",
    "Two claps and I appear. Like magic.",
    "Claude and Antigravity, coming right up.",
    "Master Tanish, your tools are ready.",
]

def install_startup():
    script_path = os.path.abspath(__file__)
    python_path = sys.executable

    startup_folder = os.path.join(
        os.environ["APPDATA"],
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )
    bat_path = os.path.join(startup_folder, "clap_launcher.bat")
    bat_content = f'@echo off\nstart "" /min "{python_path}" "{script_path}"\n'

    with open(bat_path, "w") as f:
        f.write(bat_content)

    print(f"[INSTALLED] Startup entry created at:\n  {bat_path}")
    print("[INFO] Script will now run automatically on every boot.")
    print("[INFO] To uninstall, delete that .bat file.")

def is_antigravity_running():
    for proc in psutil.process_iter(["name"]):
        try:
            if "antigravity" in proc.info["name"].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def is_claude_running():
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"].lower() == "claude.exe":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def speak(text):
    print(f"[VOICE] {text}")
    subprocess.run(
        ["powershell", "-Command",
         f'Add-Type -AssemblyName System.Speech; '
         f'$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
         f'$s.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female); '
         f'$s.Speak("{text}")'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def get_line():
    if not os.path.exists(FLAG_FILE):
        with open(FLAG_FILE, "w") as f:
            f.write("done")
        return "Opening master"
    else:
        return random.choice(CATCHY_LINES)

def open_apps():
    line = get_line()
    speak(line)
    print("[TRIGGERED] Opening Claude and Antigravity...")
    subprocess.Popen([CLAUDE_PATH])
    subprocess.run(
        ["powershell", "-Command", f'Start-Process "{ANTIGRAVITY_PATH}"'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def wait_until_either_closed():
    print("[WATCHING] Waiting for Claude or Antigravity to be closed...")
    time.sleep(6)

    while True:
        ag  = is_antigravity_running()
        cla = is_claude_running()
        print(f"  [STATUS] Antigravity={ag}  Claude={cla}")
        if not ag or not cla:
            print("[READY] An app was closed. Re-arming...\n")
            return
        time.sleep(CHECK_INTERVAL)

def is_clap(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    peak = np.max(np.abs(audio_data))
    return peak > CLAP_THRESHOLD

def listen():
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    last_clap_time    = 0
    last_trigger_time = 0
    clap_count        = 0
    armed             = True

    print(f"[LISTENING] Waiting for double claps... (threshold={CLAP_THRESHOLD})")
    print("  Tip: Lower CLAP_THRESHOLD if claps are not detected.")
    print("  Tip: Raise CLAP_THRESHOLD if noise is triggering it.")
    print("  Press Ctrl+C to stop.\n")

    try:
        while True:
            if not armed:
                stream.stop_stream()
                wait_until_either_closed()
                stream.start_stream()
                last_clap_time    = 0
                last_trigger_time = 0
                clap_count        = 0
                armed             = True
                print("[LISTENING] Re-armed. Waiting for double claps...")

            data = stream.read(CHUNK, exception_on_overflow=False)
            now  = time.time()

            if is_clap(data):
                if now - last_clap_time < 0.1:
                    continue

                gap            = now - last_clap_time
                last_clap_time = now

                if gap < DOUBLE_CLAP_GAP:
                    clap_count += 1
                else:
                    clap_count = 1

                print(f"  [CLAP] #{clap_count}  (gap={gap:.2f}s)")

                if clap_count >= 2:
                    clap_count = 0
                    if now - last_trigger_time > COOLDOWN:
                        last_trigger_time = now
                        open_apps()
                        armed = False
                    else:
                        remaining = COOLDOWN - (now - last_trigger_time)
                        print(f"  [COOLDOWN] Wait {remaining:.1f}s")

    except KeyboardInterrupt:
        print("\n[STOPPED]")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

if __name__ == "__main__":
    if "--install" in sys.argv:
        install_startup()
    else:
        listen()