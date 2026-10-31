import os
import time
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from assets.config import AUDIO_TYPES
from core.core_audio import worker
from ui.theme_manager import theme

class AppLogic:
    def __init__(self, root, files_section, progress_section, btn_theme, header):
        self.root = root
        self.files_section = files_section
        self.progress_section = progress_section
        self.btn_theme = btn_theme
        self.header = header
        
        self.output_folder = ""
        self.events = queue.Queue()
        self.is_running = False

    def log_message(self, text, level="info"):
        timestamp = time.strftime("%H:%M:%S")
        log_widget = self.progress_section.log_text
        log_widget.configure(state="normal")
        log_widget.insert(tk.END, f"[{timestamp}] ", "time")
        log_widget.insert(tk.END, text + "\n", level)
        log_widget.see(tk.END)
        log_widget.configure(state="disabled")

    def update_theme(self):
        self.root.configure(fg_color=theme.color("bg"))
        self.btn_theme.configure(
            text="☀  Light" if theme.mode == "dark" else "☾  Dark",
            fg_color=theme.color("accent_bg"), 
            hover_color=theme.color("border"), 
            text_color=theme.color("accent_text")
        )
        self.files_section.apply_theme()
        self.progress_section.apply_theme()
        self.header.configure(fg_color="transparent")

    def toggle_theme(self):
        theme.toggle()
        self.update_theme()
        self.log_message("Theme changed.")

    def choose_audio_files(self):
        if self.is_running: return
        files = filedialog.askopenfilenames(title="Select audio files", initialdir=os.getcwd(), filetypes=AUDIO_TYPES)
        if files:
            self.files_section.selected_files = list(dict.fromkeys(self.files_section.selected_files + list(files)))
            self.files_section.refresh_list()
            self.progress_section.status_var.set(f"Selected files: {len(self.files_section.selected_files)}")

    def add_youtube_link(self):
        url = self.files_section.url_var.get().strip()
        if not url or url == "Paste YouTube link...": return
        if not (url.startswith("http://") or url.startswith("https://")):
            messagebox.showwarning("Invalid Link", "Please provide a valid URL.", parent=self.root)
            return
        if url not in self.files_section.selected_files:
            self.files_section.selected_files.append(url)
            self.files_section.refresh_list()
        self.files_section.url_var.set("")
        self.files_section._on_entry_focus_out(None)

    def choose_output_folder(self):
        if self.is_running: return
        folder = filedialog.askdirectory(title="Select output folder", initialdir=self.output_folder or os.getcwd(), mustexist=True)
        if folder:
            self.output_folder = folder
            self.progress_section.folder_var.set(folder)
            self.progress_section.status_var.set("Output folder selected.")
            self.log_message(f"Output folder: {folder}")

    def start_transcription(self):
        if self.is_running or not self.files_section.selected_files or not self.output_folder:
            messagebox.showwarning("Missing Data", "Please select files and an output folder.", parent=self.root)
            return

        self.is_running = True
        self._set_ui_state("disabled")
        
        self.progress_section.progress_var.set(0)
        self.log_message("Starting transcription...")

        threading.Thread(
            target=worker, 
            args=(self.files_section.selected_files.copy(), self.output_folder, self.events), 
            daemon=True
        ).start()

    def _set_ui_state(self, state):
        """Pomocnicza funkcja do blokowania/odblokowywania przycisków"""
        self.files_section.btn_choose.configure(state=state)
        self.files_section.btn_add_url.configure(state=state)
        self.files_section.entry_url.configure(state=state)
        self.progress_section.btn_folder.configure(state=state)
        self.progress_section.btn_start.configure(state=state)
        self.btn_theme.configure(state="normal") # Motyw zawsze aktywny

    def process_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                kind = event[0]
                
                if kind == "status": 
                    self.progress_section.status_var.set(event[1])
                elif kind == "progress":
                    self.progress_section.progress_var.set(event[1] / 100)
                    self.progress_section.percent_var.set(f"{int(event[1])}%")
                    self.progress_section.status_var.set(event[2])
                elif kind == "log": 
                    self.log_message(event[1])
                elif kind == "warning":
                    self.progress_section.status_var.set(event[1])
                    self.log_message(event[1], "warning")
                elif kind == "error": 
                    self.log_message(event[1], "error")
                elif kind == "finished":
                    self.progress_section.status_var.set(event[1])
                    messagebox.showinfo("Transcription", event[1], parent=self.root)
                elif kind == "worker_stopped":
                    self.is_running = False
                    self._set_ui_state("normal")
        except queue.Empty:
            pass
        
        self.root.after(150, self.process_events)