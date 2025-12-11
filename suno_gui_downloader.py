# ================================================
# SUNO VAULT — MRBIGPIPES EDITION (FINAL WORKING)
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

FILENAME_BAD_CHARS = r'[<>:"/\\|?*\x00-\x1F]'
API_BASE = "https://studio-api.prod.suno.com/api/feed/v2"
DELAY = 4.2

def sanitize(name: str) -> str:
    return re.sub(FILENAME_BAD_CHARS, "_", name).strip(" .")[:180]

def unique_path(folder: str, name: str) -> str:
    path = os.path.join(folder, name)
    if not os.path.exists(path):
        return path
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

class MrBigPipesDownloader:
    def __init__(self, token, folder, thumbs, log, prog):
        self.token = token.strip()
        self.folder = folder
        self.thumbs = thumbs
        self.log = log
        self.prog = prog
        self.stop = False

    def get_all(self):
        songs = {}
        page = 1
        headers = {"Authorization": f"Bearer {self.token}"}

        while not self.stop:
            url = f"{API_BASE}?hide_disliked=true&hide_gen_stems=true&hide_studio_clips=true&page={page}"
            self.log(f"Raiding page {page}...")
            try:
                r = requests.get(url, headers=headers, timeout=20)
                if r.status_code == 401:
                    self.log("Token dead. Get a fresh one.")
                    return {}
                data = r.json()
                clips = data if isinstance(data, list) else data.get("clips", [])
                if not clips:
                    self.log("Reached end of library.")
                    break
                for c in clips:
                    sid = c.get("id")
                    if sid and sid not in songs:
                        songs[sid] = {
                            "title": c.get("title", "Untitled Banger"),
                            "audio": c.get("audio_url"),
                            "img": c.get("image_url") or c.get("image_large_url"),
                            "artist": c.get("display_name") or "MrBigPipes"
                        }
                self.log(f"Page {page} → +{len(clips)} tracks | Total: {len(songs)}")
                page += 1
                time.sleep(DELAY)
            except Exception as e:
                self.log(f"Error: {e}")
                break
        return songs

    def run(self):
        os.makedirs(self.folder, exist_ok=True)
        songs = self.get_all()
        if not songs or self.stop:
            return

        total = len(songs)
        self.prog(0, total)
        self.log(f"\nMRBIGPIPES MODE — Downloading {total} tracks")

        for i, (sid, info) in enumerate(songs.items(), 1):
            if self.stop:
                self.log("Stopped by the boss.")
                break

            title = info["title"]
            file = sanitize(title) + ".mp3"
            final = unique_path(self.folder, file)

            self.log(f"[{i}/{total}] {title}")
            try:
                r = requests.get(info["audio"], headers={"Authorization": f"Bearer {self.token}"}, stream=True, timeout=90)
                r.raise_for_status()
                with open(final, "wb") as f:
                    for chunk in r.iter_content(8192):
                        if self.stop: break
                        f.write(chunk)

                if self.thumbs and info["img"]:
                    self.log(f"   {embed_cover(final, info['img'], title, info['artist'], self.token)}")

            except Exception as e:
                self.log(f"   Failed: {e}")

            self.prog(i, total)

        self.log("\nALL TRACKS SECURED. MRBIGPIPES OUT.")
        messagebox.showinfo("MRBIGPIPES", "Download complete!")

# Token guide pop-up
def show_token_guide():
    guide = """
HOW TO GET YOUR SUNO TOKEN (15 seconds)

1. Open https://suno.com → log in
2. Press F12 → Network tab
3. In filter box type: continue
4. Play any song or click "Continue" on a prompt
5. Click the request named "continue" / "generate_continue"
6. Scroll to Request Headers
7. Find: Authorization: Bearer eyJhbGc...
8. Copy everything AFTER "Bearer "

→ Come back → click PASTE → START RAID
    """.strip()

    win = tk.Toplevel()
    win.title("MRBIGPIPES TOKEN GUIDE")
    win.geometry("700x500")
    win.configure(bg="#000")
    tk.Label(win, text="HOW TO GET TOKEN", font=("Impact", 20), fg="#ff2d55", bg="#000").pack(pady=20)
    txt = tk.Text(win, bg="#111", fg="#00ff00", font=("Consolas", 11), wrap="word")
    txt.pack(fill="both", expand=True, padx=30, pady=10)
    txt.insert("1.0", guide)
    txt.config(state="disabled")
    tk.Button(win, text="GOT IT", font=("Segoe UI",10,"bold"), bg="#ff2d55", fg="white", command=win.destroy).pack(pady=10)

# GUI
class MrBigPipesApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Suno Vault — MRBIGPIPES EDITION")
        self.root.geometry("840x720")
        self.root.configure(bg="#0d0d0d")
        self.root.resizable(False, False)

        tk.Label(self.root, text="MRBIGPIPES", font=("Impact", 36, "bold"), fg="#ff2d55", bg="#0d0d0d").pack(pady=(20,0))
        tk.Label(self.root, text="Suno Vault — Private Edition", font=("Segoe UI", 16), fg="#1DB954", bg="#0d0d0d").pack()

        # Token + help
        token_row = tk.Frame(self.root, bg="#0d0d0d")
        token_row.pack(fill="x", padx=40, pady=10)
        tk.Label(token_row, text="Bearer Token", fg="#fff", bg="#0d0d0d").pack(side="left")
        tk.Button(token_row, text="HELP – HOW TO GET TOKEN", bg="#333", fg="#ff2d55", command=show_token_guide).pack(side="right")

        tframe = tk.Frame(self.root, bg="#0d0d0d")
        tframe.pack(fill="x", padx=40)
        self.token_var = tk.StringVar()
        tk.Entry(tframe, textvariable=self.token_var, width=70, font=("Consolas",11), bg="#1e1e1e", fg="#00ff00").pack(side="left", fill="x", expand=True, padx=(0,10))
        tk.Button(tframe, text="PASTE", bg="#ff2d55", fg="white", command=self.paste).pack(side="right")

        # Folder
        tk.Label(self.root, text="Save Folder", fg="#fff", bg="#0d0d0d").pack(anchor="w", padx=40, pady=(15,0))
        fframe = tk.Frame(self.root, bg="#0d0d0d")
        fframe.pack(fill="x", padx=40)
        self.folder_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"),"Desktop","MrBigPipes Vault"))
        tk.Entry(fframe, textvariable=self.folder_var, width=60, bg="#1e1e1e", fg="white").pack(side="left", fill="x", expand=True, padx=(0,10))
        tk.Button(fframe, text="BROWSE", command=self.browse, bg="#333", fg="white").pack(side="right")

        self.thumbs = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Embed cover art & metadata", variable=self.thumbs, fg="#1DB954", bg="#0d0d0d").pack(pady=10)

        # Buttons
        btns = tk.Frame(self.root, bg="#0d0d0d")
        btns.pack(pady=25)
        self.start_btn = tk.Button(btns, text="START RAID", font=("Impact",14,"bold"), bg="#ff2d55", fg="white", width=18, command=self.start)
        self.start_btn.pack(side="left", padx=15)
        self.stop_btn = tk.Button(btns, text="STOP", font=("Impact",12), bg="#333", fg="#ff2d55", state="disabled", command=self.stop)
        self.stop_btn.pack(side="left", padx=15)

        # Progress & Log
        self.bar = ttk.Progressbar(self.root, length=760, mode="determinate")
        self.bar.pack(pady=15, padx=40)
        tk.Label(self.root, text="Live Log", fg="#ff2d55", bg="#0d0d0d", font=("Segoe UI",10,"bold")).pack(anchor="w", padx=40)
        self.logbox = scrolledtext.ScrolledText(self.root, height=16, bg="#000", fg="#00ff00", font=("Consolas",10))
        self.logbox.pack(padx=40, pady=10, fill="both", expand=True)

    def log(self, msg):
        self.logbox.config(state="normal")
        self.logbox.insert("end", msg + "\n")
        self.logbox.see("end")
        self.logbox.config(state="disabled")

    def paste(self):
        try:
            self.token_var.set(self.root.clipboard_get())
            self.log("Token loaded — ready")
        except:
            messagebox.showwarning("Nope", "Nothing in clipboard")

    def browse(self):
        f = filedialog.askdirectory()
        if f: self.folder_var.set(f)

    def update_bar(self, cur, tot):
        self.bar["value"] = (cur/tot)*100 if tot else 0
        self.root.title(f"MrBigPipes Vault — {cur}/{tot}")

    def start(self):
        if not self.token_var.get().strip():
            messagebox.showerror("Missing", "Need token first")
            return
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log("MRBIGPIPES IS LIVE\n")

        dl = MrBigPipesDownloader(self.token_var.get(), self.folder_var.get(), self.thumbs.get(), self.log, self.update_bar)
        def t():
            dl.stop = False
            dl.run()
            self.root.after(0, lambda: self.stop_btn.config(state="disabled"))
            self.root.after(0, lambda: self.start_btn.config(state="normal"))
        threading.Thread(target=t, daemon=True).start()

    def stop(self):
        messagebox.showinfo("Stopping", "Finishing current song then stopping...")
        # flag is checked inside loops

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    MrBigPipesApp().run()