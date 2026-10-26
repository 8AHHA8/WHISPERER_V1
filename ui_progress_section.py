# ui_progress_section.py
import customtkinter as ctk
import tkinter as tk
from theme_manager import theme

class ProgressSection:
    def __init__(self, parent):
        self.card_folder = self._make_card(parent, "2.  Output Folder")
        self._build_folder(self.card_folder)
        
        self.card_progress = self._make_card(parent, "3.  Transcription & Progress")
        self._build_progress(self.card_progress)
        
        self.card_log = self._make_card(parent, "Log Messages", expand=True)
        self._build_log(self.card_log)

    def _make_card(self, parent, title, expand=False):
        card = ctk.CTkFrame(parent, fg_color=theme.color("surface"), border_color=theme.color("border"), border_width=1, corner_radius=15)
        card.pack(fill="both" if expand else "x", expand=expand, pady=(0, 8))
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 12, "bold"), text_color=theme.color("text")).pack(anchor="w", padx=13, pady=(11, 7))
        return card

    def _build_folder(self, card):
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(0, 12))
        
        self.btn_folder = ctk.CTkButton(row, text="▣  Select Folder", height=36, corner_radius=11, fg_color=theme.color("accent_bg"), hover_color=theme.color("border"), text_color=theme.color("accent_text"), font=("Segoe UI", 12, "bold"))
        self.btn_folder.pack(side="left", padx=(0, 10))
        
        self.folder_var = tk.StringVar(value="No folder selected")
        self.lbl_folder = ctk.CTkLabel(row, textvariable=self.folder_var, text_color=theme.color("muted"), font=("Segoe UI", 12), anchor="w", wraplength=400)
        self.lbl_folder.pack(side="left", fill="x", expand=True)

    def _build_progress(self, card):
        self.btn_start = ctk.CTkButton(card, text="▶   Start Transcription", height=36, corner_radius=11, fg_color=theme.color("primary"), hover_color=theme.color("primary_hover"), text_color="#FFFFFF", font=("Segoe UI", 12, "bold"))
        self.btn_start.pack(fill="x", padx=12, pady=(0, 12))
        
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(0, 5))
        
        self.progress_var = tk.DoubleVar(value=0)
        self.bar = ctk.CTkProgressBar(row, variable=self.progress_var, height=10, corner_radius=7, fg_color=theme.color("progress_bg"), progress_color=theme.color("primary"))
        self.bar.pack(side="left", fill="x", expand=True)
        self.bar.set(0)
        
        self.percent_var = tk.StringVar(value="0%")
        self.lbl_percent = ctk.CTkLabel(row, textvariable=self.percent_var, width=40, text_color=theme.color("accent_text"), font=("Segoe UI", 12, "bold"))
        self.lbl_percent.pack(side="right", padx=(8, 0))
        
        self.status_var = tk.StringVar(value="Ready.")
        self.lbl_status = ctk.CTkLabel(card, textvariable=self.status_var, text_color=theme.color("muted"), font=("Segoe UI", 12), anchor="w", wraplength=680)
        self.lbl_status.pack(fill="x", padx=12, pady=(2, 12))

    def _build_log(self, card):
        self.log_text = ctk.CTkTextbox(card, height=80, corner_radius=10, border_width=1, border_color=theme.color("border"), fg_color=theme.color("log_bg"), text_color=theme.color("text"), font=("Segoe UI", 12), wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.log_text.configure(state="disabled")
        self.log_text.tag_config("time", foreground=theme.color("muted"))
        self.log_text.tag_config("info", foreground=theme.color("text"))
        self.log_text.tag_config("warning", foreground=theme.color("warning"))
        self.log_text.tag_config("error", foreground=theme.color("danger"))
        
    def apply_theme(self):
        self.card_folder.configure(fg_color=theme.color("surface"), border_color=theme.color("border"))
        self.btn_folder.configure(fg_color=theme.color("accent_bg"), hover_color=theme.color("border"), text_color=theme.color("accent_text"))
        self.lbl_folder.configure(text_color=theme.color("muted"))
        
        self.card_progress.configure(fg_color=theme.color("surface"), border_color=theme.color("border"))
        self.btn_start.configure(fg_color=theme.color("primary"), hover_color=theme.color("primary_hover"))
        self.bar.configure(fg_color=theme.color("progress_bg"), progress_color=theme.color("primary"))
        self.lbl_percent.configure(text_color=theme.color("accent_text"))
        self.lbl_status.configure(text_color=theme.color("muted"))
        
        self.card_log.configure(fg_color=theme.color("surface"), border_color=theme.color("border"))
        self.log_text.configure(fg_color=theme.color("log_bg"), text_color=theme.color("text"), border_color=theme.color("border"))
        self.log_text.tag_config("time", foreground=theme.color("muted"))
        self.log_text.tag_config("info", foreground=theme.color("text"))
        self.log_text.tag_config("warning", foreground=theme.color("warning"))
        self.log_text.tag_config("error", foreground=theme.color("danger"))