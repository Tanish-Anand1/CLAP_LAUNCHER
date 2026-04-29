# 👏 Clap Launcher

A lightweight, audio-activated automation script that launches your favorite development tools simply by clapping twice.

![Banner](https://img.shields.io/badge/Status-Active-brightgreen.svg) ![Platform](https://img.shields.io/badge/Platform-Windows-blue.svg) ![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)

---

## 📖 Overview

**Clap Launcher** allows you to open predefined applications—such as Claude AI and Antigravity—with a simple double-clap. Using your microphone, it listens for acoustic peaks and triggers your workflow instantly, saving you time and giving your workstation a futuristic feel.

It comes equipped with an easy installation command to run automatically on Windows startup.

## ✨ Features

- **Acoustic Activation:** Triggers specifically on double claps (configurable gap and threshold).
- **Smart Resource Management:** Only listens when your tools are closed, pausing the microphone stream when active to save resources.
- **Voice Feedback:** Uses Windows Speech Synthesis to welcome you with catchy lines like *"Welcome back, Master. Your tools await."*
- **Auto-Start Support:** Effortlessly installs itself to the Windows Startup folder so it's always ready.
- **Configurable Sensitivities:** Easily tweak threshold, gap, and cooldown settings directly in the script.

## 🛠 Prerequisites

Make sure you have Python installed along with the following packages:

```bash
pip install pyaudio numpy psutil
```

## 🚀 Usage

### Running Normally
To just run the script and start listening for claps:

```bash
python script.py
```

### Installing on Startup
To configure the script to launch automatically every time you start your computer:

```bash
python script.py --install
```
This creates a lightweight `.bat` file in your Windows Startup directory.

## ⚙️ Configuration

You can tweak the variables in the `# ── CONFIG ──` section of `script.py` to match your environment:

- `CLAP_THRESHOLD` (Default `3000`): Adjust this depending on your microphone sensitivity and background noise.
- `DOUBLE_CLAP_GAP` (Default `0.6`): Maximum time allowed between two claps to trigger the launcher.
- `COOLDOWN` (Default `3.0`): Wait time before another trigger can occur.

You can also update the paths for the applications it opens:
- `CLAUDE_PATH`
- `ANTIGRAVITY_PATH`

## 🗑 Uninstallation

If you wish to remove the script from running on startup, simply delete the `clap_launcher.bat` file from:
`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

## 📜 License

This project is open-source and free to use. Feel free to modify and expand its capabilities!
