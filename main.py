import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_OFFLINE"] = "0"

import sys
from pathlib import Path

nvidia_path = Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
if nvidia_path.exists():
    for folder in nvidia_path.iterdir():
        if folder.is_dir() and (folder / "bin").exists():
            os.add_dll_directory(str(folder / "bin"))
            os.environ["PATH"] = str(folder / "bin") + os.pathsep + os.environ["PATH"]

import customtkinter as ctk
from ui.theme_manager import theme
from ui.ui_files_section import FilesSection
from ui.ui_progress_section import ProgressSection
from app.logic import AppLogic

root = ctk.CTk()
root.title("WHISPERER_V1")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root.iconbitmap(resource_path("assets/purple_pen.ico"))
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

header = ctk.CTkFrame(main_frame, fg_color="transparent")
header.pack(fill="x", pady=(0, 10))

btn_theme = ctk.CTkButton(header, text="☾  Dark", width=96, height=33, corner_radius=10)
btn_theme.pack(side="right")

files_section = FilesSection(main_frame)
progress_section = ProgressSection(main_frame)

app = AppLogic(root, files_section, progress_section, btn_theme, header)

btn_theme.configure(command=app.toggle_theme)
files_section.btn_choose.configure(command=app.choose_audio_files)
files_section.btn_add_url.configure(command=app.add_youtube_link)
progress_section.btn_folder.configure(command=app.choose_output_folder)
progress_section.btn_start.configure(command=app.start_transcription)

app.update_theme()
app.log_message("Application ready.")
app.process_events()

root.mainloop()