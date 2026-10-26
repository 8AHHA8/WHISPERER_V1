import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_OFFLINE"] = "0"

import sys
from pathlib import Path

# Dodaje foldery NVIDIA do ścieżki wyszukiwania DLL
nvidia_path = Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
if nvidia_path.exists():
    for folder in nvidia_path.iterdir():
        if folder.is_dir() and (folder / "bin").exists():
            os.add_dll_directory(str(folder / "bin"))
            os.environ["PATH"] = str(folder / "bin") + os.pathsep + os.environ["PATH"]

import time
import queue
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox

from config import AUDIO_TYPES
from core_audio import worker
from theme_manager import theme
from ui_files_section import FilesSection
from ui_progress_section import ProgressSection

# Zmienne stanu
output_folder = ""
events = queue.Queue()
is_running = False

# --- INICJALIZACJA OKNA ---
root = ctk.CTk()
root.title("WHISPERER_V1")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root.iconbitmap(resource_path("purple_pen.ico"))
ctk.set_appearance_mode(theme.mode)

window_width = 760
window_height = 1000
root.update_idletasks()
screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
window_width, window_height = min(window_width, screen_w - 40), min(window_height, screen_h - 60)
x, y = max(0, (screen_w - window_width) // 2), max(0, (screen_h - window_height) // 2 - 15)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.minsize(580, 650)

main_frame = ctk.CTkFrame(root, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=16, pady=12)

# --- FUNKCJE LOGIKI ---

def log_message(text, level="info"):
    timestamp = time.strftime("%H:%M:%S")
    log_widget = progress_section.log_text
    log_widget.configure(state="normal")
    log_widget.insert(tk.END, f"[{timestamp}] ", "time")
    log_widget.insert(tk.END, text + "\n", level)
    log_widget.see(tk.END)
    log_widget.configure(state="disabled")

def update_theme():
    root.configure(fg_color=theme.color("bg"))
    btn_theme.configure(
        text="☀  Light" if theme.mode == "dark" else "☾  Dark",
        fg_color=theme.color("accent_bg"), 
        hover_color=theme.color("border"), 
        text_color=theme.color("accent_text")
    )
    files_section.apply_theme()
    progress_section.apply_theme()
    
    header.configure(fg_color="transparent")

def toggle_theme():
    theme.toggle()
    update_theme()
    log_message("Theme changed.")

def choose_audio_files():
    if is_running: return
    files = filedialog.askopenfilenames(title="Select audio files", initialdir=os.getcwd(), filetypes=AUDIO_TYPES)
    if files:
        files_section.selected_files = list(dict.fromkeys(files_section.selected_files + list(files)))
        files_section.refresh_list()
        progress_section.status_var.set(f"Selected files: {len(files_section.selected_files)}")

def add_youtube_link():
    url = files_section.url_var.get().strip()
    if not url or url == "Paste YouTube link...": return
    if not (url.startswith("http://") or url.startswith("https://")):
        messagebox.showwarning("Invalid Link", "Please provide a valid URL.", parent=root)
        return
    if url not in files_section.selected_files:
        files_section.selected_files.append(url)
        files_section.refresh_list()
    files_section.url_var.set("")
    files_section._on_entry_focus_out(None) # Resetuje placeholder

def choose_output_folder():
    global output_folder
    if is_running: return
    folder = filedialog.askdirectory(title="Select output folder", initialdir=output_folder or os.getcwd(), mustexist=True)
    if folder:
        output_folder = folder
        progress_section.folder_var.set(folder)
        progress_section.status_var.set("Output folder selected.")
        log_message(f"Output folder: {folder}")

def start_transcription():
    global is_running
    if is_running or not files_section.selected_files or not output_folder:
        messagebox.showwarning("Missing Data", "Please select files and an output folder.", parent=root)
        return

    is_running = True
    files_section.btn_choose.configure(state="disabled")
    files_section.btn_add_url.configure(state="disabled")
    files_section.entry_url.configure(state="disabled")
    progress_section.btn_folder.configure(state="disabled")
    progress_section.btn_start.configure(state="disabled")
    btn_theme.configure(state="normal")
    
    progress_section.progress_var.set(0)
    log_message("Starting transcription...")

    threading.Thread(target=worker, args=(files_section.selected_files.copy(), output_folder, events), daemon=True).start()

def process_events():
    global is_running
    try:
        while True:
            event = events.get_nowait()
            kind = event[0]
            if kind == "status": progress_section.status_var.set(event[1])
            elif kind == "progress":
                progress_section.progress_var.set(event[1] / 100)
                progress_section.percent_var.set(f"{int(event[1])}%")
                progress_section.status_var.set(event[2])
            elif kind == "log": log_message(event[1])
            elif kind == "warning":
                progress_section.status_var.set(event[1])
                log_message(event[1], "warning")
            elif kind == "error": log_message(event[1], "error")
            elif kind == "finished":
                progress_section.status_var.set(event[1])
                messagebox.showinfo("Transcription", event[1], parent=root)
            elif kind == "worker_stopped":
                is_running = False
                files_section.btn_choose.configure(state="normal")
                files_section.btn_add_url.configure(state="normal")
                files_section.entry_url.configure(state="normal")
                progress_section.btn_folder.configure(state="normal")
                progress_section.btn_start.configure(state="normal")
    except queue.Empty:
        pass
    root.after(150, process_events)

# --- BUDOWA INTERFEJSU ---

header = ctk.CTkFrame(main_frame, fg_color="transparent")
header.pack(fill="x", pady=(0, 10))

btn_theme = ctk.CTkButton(header, text="☾  Dark", width=96, height=33, corner_radius=10, command=toggle_theme)
btn_theme.pack(side="right")

files_section = FilesSection(main_frame)
files_section.btn_choose.configure(command=choose_audio_files)
files_section.btn_add_url.configure(command=add_youtube_link)

progress_section = ProgressSection(main_frame)
progress_section.btn_folder.configure(command=choose_output_folder)
progress_section.btn_start.configure(command=start_transcription)

# --- START ---
update_theme()
log_message("Application ready.")
root.after(150, process_events)
root.mainloop()