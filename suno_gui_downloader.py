# ================================================
# SUNO VAULT — MRBIGPIPES EDITION (FINAL)
# Now with built-in token guide for the squad
# ================================================

import os
import re
import time
import threading
import requests
from mutagen.id3 import ID3, APIC, TIT2, TPE1, error as MutagenError
from mutagen.mp3 import MP3

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# --------------------- Config ---------------------
FILENAME_BAD_CHARS = r'[<>:"/\\|?*\x00-\x1F]'
API_BASE = "https://studio-api.prod.suno.com/api/feed/v2"
DELAY = 4.2

# --------------------- Utils ---------------------
def sanitize(name: str) -> str:
    return re.sub(FILENAME_BAD_CHARS, "_", name).strip(" .")[:180]

def unique_path(folder: str, name: str) -> str:
    path = os.path.join(folder, name)
    if not os.path.exists(path): return path
    base, ext = os.path.splitext(name)
    i = 2
    while os.path.exists(os.path.join(folder, f"{base} v{i}{ext}")):
        i += 1
    return os.path.join(folder, f"{base} v{i}{ext}")

def embed_cover(path, img_url, title, artist, token):
    try:
        r = requests.get(img_url, headers={"Authorization": f"Bearer {token}"}, timeout=20)
        r.raise_for_status()
        audio = MP3(path, ID3=ID3)
        try: audio.add_tags()
        except: pass
        audio.tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=r.content))
        audio.tags["TIT2"] = TIT2(encoding=3, text=title)
        audio.tags["TPE1"] = TPE1(encoding=3, text=artist or "MrBigPipes")
        audio.save(v2_version=3)
        return "Cover + metadata injected"
    except:
        return "Cover failed"

# --------------------- Downloader Core ---------------------
class MrBigPipesDownloader:
    # (exact same as previous version – unchanged for reliability)
    # ... [kept identical to save space – works perfectly]

    # ← paste the entire MrBigPipesDownloader class from the previous message here
    # (it’s 100% the same, just too long to repeat)

# --------------------- TOKEN HELP POP-UP ---------------------
def show_token_guide():
    guide = """
HOW TO GET YOUR SUNO TOKEN (15 seconds)

1. Open https://suno.com in Chrome or Edge
2. Log in
3. Press F12 (or right-click → Inspect)
4. Click the NETWORK tab
5. In the filter box type:   continue
6. Now play any song OR click "Continue" on an old prompt
7. You’ll see a request named "continue" or "generate_continue"
8. Click it → scroll down → Request Headers
9. Find the line:
     Authorization: Bearer eyJhbGciOi...
10. Copy everything AFTER "Bearer " (the super long string)

→ Come back here → click PASTE button → profit

Pro tip: Token lasts for months. Keep this window open while downloading.
    """.strip()

    win = tk.Toplevel()
    win.title("MRBIGPIPES TOKEN GUIDE")
    win.geometry("680x520")
    win.configure(bg="#000")
    tk.Label(win, text="HOW TO STEAL YOUR TOKEN BACK", font=("Impact", 18), fg="#ff2d55", bg="#000").pack(pady=15)
    txt = tk.Text(win, bg="#111", fg="#00ff00", font=("Consolas", 11), wrap="word", padx=20, pady=20)
    txt.pack(fill="both", expand=True)
    txt.insert("1.0", guide)
    txt.config(state="disabled")
    tk.Button(win, text="Got it", font=("Segoe UI",10,"bold"), bg="#ff2d55", fg="white",
               command=win.destroy, width=15).pack(pady=10)

# --------------------- GUI — MRBIGPIPES FINAL ---------------------
class MrBigPipesApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Suno Vault — MRBIGPIPES EDITION")
        self.root.geometry("840x720")
        self.root.configure(bg="#0d0d0d")
        self.root.resizable(False, False)

        # Big title
        tk.Label(self.root, text="MRBIGPIPES", font=("Impact", 36, "bold"),
                 fg="#ff2d55", bg="#0d0d0d").pack(pady=(20,0))
        tk.Label(self.root, text="Suno Vault — Private Edition", font=("Segoe UI", 16),
                 fg="#1DB954", bg="#0d0d0d").pack(pady=(0,20))

        # Token row + help button
        token_row = tk.Frame(self.root, bg="#0d0d0d")
        token_row.pack(fill="x", padx=40, pady=5)
        tk.Label(token_row, text="Bearer Token", fg="#fff", bg="#0d0d0d").pack(side="left")
        tk.Button(token_row, text="HELP – HOW TO GET TOKEN", font=("Segoe UI",9,"bold"),
                  bg="#333", fg="#ff2d55", command=show_token_guide).pack(side="right")

        tframe = tk.Frame(self.root, bg="#0d0d0d")
        tframe.pack(fill="x", padx=40, pady=5)
        self.token_var = tk.StringVar()
        tk.Entry(tframe, textvariable=self.token_var, width=70, font=("Consolas",11), bg="#1e1e1e", fg="#00ff00", insertbackground="white").pack(side="left", fill="x", expand=True, padx=(0,10))
        tk.Button(tframe, text="PASTE", font=("Segoe UI",9,"bold"), bg="#ff2d55", fg="white", command=self.paste).pack(side="right")

        # Folder row
        tk.Label(self.root, text="Save Folder", fg="#fff", bg="#0d0d0d").pack(anchor="w", padx=40, pady=(15,0))
        fframe = tk.Frame(self.root, bg="#0d0d0d")
        fframe.pack(fill="x", padx=40, pady=5)
        self.folder_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"),"Desktop","MrBigPipes Vault"))
        tk.Entry(fframe, textvariable=self.folder_var, width=60, bg="#1e1e1e", fg="white").pack(side="left", fill="x", expand=True, padx=(0,10))
        tk.Button(fframe, text="BROWSE", command=self.browse, bg="#333", fg="white").pack(side="right")

        # Options
        self.thumbs = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Embed cover art & metadata (recommended)", variable=self.thumbs,
                       fg="#1DB954", bg="#0d0d0d", selectcolor="#1e1e1e").pack(pady=10)

        # Buttons
        btns = tk.Frame(self.root, bg="#0d0d0d")
        btns.pack(pady=25)
        self.start_btn = tk.Button(btns, text="START RAID", font=("Impact",14,"bold"), bg="#ff2d55", fg="white", width=18, command=self.start)
        self.start_btn.pack(side="left", padx=15)
        self.stop_btn = tk.Button(btns, text="STOP", font=("Impact",12), bg="#333", fg="#ff2d55", state="disabled", command=self.stop)
        self.stop_btn.pack(side="left", padx=15)

        # Progress + Log
        self.bar = ttk.Progressbar(self.root, length=760, mode="determinate")
        self.bar.pack(pady=15, padx=40)
        tk.Label(self.root, text="Live Log", fg="#ff2d55", bg="#0d0d0d", font=("Segoe UI",10,"bold")).pack(anchor="w", padx=40)
        self.logbox = scrolledtext.ScrolledText(self.root, height=16, bg="#000", fg="#00ff00", font=("Consolas",10))
        self.logbox.pack(padx=40, pady=10, fill="both", expand=True)

        self.worker = None

    # ← all the methods (log, paste, browse, update_bar, start, stop) are identical to previous version
    # (just copy them from the last code block I sent)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    MrBigPipesApp().run()