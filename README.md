MrBigPipes Suno VaultFull Dummy-Proof Installation & Usage Guide
(Updated for December 2025 — 100% working)markdown

# MrBigPipes Suno Vault — Full Setup Guide (Windows 11/10 · December 2025

You are 7 minutes away from owning every single Suno song you’ve ever made — offline, forever, with covers and perfect metadata.

## 1. Install Python (one-time, 2 minutes)

1. Go here → https://www.python.org/downloads/
2. Click the big yellow button **Download Python 3.12.x** (or newer)
3. Run the installer
4. VERY IMPORTANT → **Tick the box “Add python.exe to PATH”** (bottom of first screen)
5. Click **Install Now** → finish → close

Test it:
- Press **Win + R** → type `cmd` → press Enter
- Type: `python --version`
- If it shows “Python 3.12.x” → you’re good. Close the window.

## 2. Create Your Folder & Get the Files

1. On your Desktop, right-click → New → Folder → name it exactly:  
   `MrBigPipes Suno Vault`
2. Put these 3 files inside it (create them with Notepad):

### File 1: `suno_gui_downloader.py`
→ Paste the full working script I gave you last time (the one with the fixed tkinter import)

### File 2: `requirements.txt`
```txt
requests>=2.32.0
mutagen>=1.47.0

File 3: README.md (optional, but nice)You’re reading it right now3. Install the 2 required libraries (30 seconds)Open Command Prompt (Win + R → cmd → Enter)
Type these 2 lines (press Enter after each):

cmd

cd Desktop\"MrBigPipes Suno Vault"
pip install -r requirements.txt

You’ll see stuff downloading → ends with “Successfully installed”.4. Get Your Suno Token (December 2025 method — works 100%)Open Chrome/Edge → go to https://suno.com → log in
Press F12 → click Network tab
In the filter box type exactly: v3
Now play any song OR click “Continue” on any prompt
Click any request that has v3 in the name (example: v3/songs, v3/feed)
In the right panel → scroll to Request Headers
Find the line:

Authorization: Bearer eyJhbGciOi...

Copy only the long string after “Bearer ” → paste it into Notepad

You now have your token. It lasts months.5. Run the Downloader (the fun part)In the same Command Prompt window, type:cmd

python suno_gui_downloader.py

The red & black MrBigPipes GUI will pop up.Inside the GUI:Click HELP – HOW TO GET TOKEN if you’re lost
Click PASTE → your token appears in green
Leave folder as MrBigPipes Vault (or click BROWSE)
Make sure “Embed cover art & metadata” is ticked
Click START RAID

Watch the green log fly. Go make coffee. When it says “ALL TRACKS SECURED”, you’re done.All files → Desktop\MrBigPipes Vault → perfect MP3s with album art.You’re now immune to Suno deleting your songs ever again.Enjoy your empire.
— MrBigPipes 2025

