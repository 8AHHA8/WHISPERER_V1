import customtkinter as ctk
import tkinter as tk
from theme_manager import theme

class FilesSection:
    def __init__(self, parent):
        self.selected_files = []
        self.file_rows = []
        self.card = self._build_card(parent)
        
    def _build_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color=theme.color("surface"), border_color=theme.color("border"), border_width=1, corner_radius=15)
        card.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(card, text="1.  Audio Files / YouTube", font=("Segoe UI", 12, "bold"), text_color=theme.color("text")).pack(anchor="w", padx=13, pady=(11, 7))
        
        self.top_frame = ctk.CTkFrame(card, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=12, pady=(0, 8))
        
        self.btn_choose = ctk.CTkButton(self.top_frame, text="＋  Audio Files", height=36, corner_radius=11, fg_color=theme.color("primary"), hover_color=theme.color("primary_hover"), text_color="#FFFFFF", font=("Segoe UI", 12, "bold"))
        self.btn_choose.pack(side="left")
        
        # Ręczny placeholder
        self.url_var = tk.StringVar(value="Paste YouTube link...")
        self.entry_url = ctk.CTkEntry(
            self.top_frame, 
            textvariable=self.url_var, 
            width=450, 
            height=36, 
            font=("Segoe UI", 12),
            text_color=theme.color("muted")
        )
        self.entry_url.pack(side="left", padx=(10, 5))
        
        self.entry_url.bind("<FocusIn>", self._on_entry_focus_in)
        self.entry_url.bind("<FocusOut>", self._on_entry_focus_out)
        self.entry_url.bind("<Enter>", self._on_entry_hover_in)   
        self.entry_url.bind("<Leave>", self._on_entry_hover_out)  
        
        self.btn_add_url = ctk.CTkButton(self.top_frame, text="Add", height=36, corner_radius=11, fg_color=theme.color("accent_bg"), hover_color=theme.color("border"), text_color=theme.color("accent_text"), font=("Segoe UI", 12, "bold"))
        self.btn_add_url.pack(side="left")
        
        self.count_var = tk.StringVar(value="0 files")
        ctk.CTkLabel(self.top_frame, textvariable=self.count_var, text_color=theme.color("muted"), font=("Segoe UI", 12)).pack(side="right")
        
        self.list_frame = ctk.CTkScrollableFrame(card, fg_color=theme.color("log_bg"), corner_radius=11, border_width=1, border_color=theme.color("border"), height=70)
        self.list_frame.pack(fill="x", expand=False, padx=12, pady=(0, 12))
        
        return card

    # --- OBSŁUGA HOVER I FOCUS DLA POLA URL ---

    def _on_entry_focus_in(self, event):
        if self.url_var.get() == "Paste YouTube link...":
            self.url_var.set("")
            self.entry_url.configure(text_color=theme.color("text"))

    def _on_entry_focus_out(self, event):
        if not self.url_var.get():
            self.url_var.set("Paste YouTube link...")
            self.entry_url.configure(text_color=theme.color("muted"))

    def _on_entry_hover_in(self, event):
        self.entry_url.configure(fg_color=theme.color("border"))

    def _on_entry_hover_out(self, event):
        self.entry_url.configure(fg_color=theme.color("surface_alt"))


    def refresh_list(self):
        for row in self.file_rows:
            row["frame"].destroy()
        self.file_rows = []

        for path in self.selected_files:
            row_frame = ctk.CTkFrame(self.list_frame, fg_color=theme.color("surface_alt"), corner_radius=10, border_width=1, border_color=theme.color("border"))
            row_frame.pack(fill="x", padx=4, pady=3)

            display_name = path if not path.startswith("http") else f"[YouTube] {path[:40]}..."
            name_label = ctk.CTkLabel(row_frame, text=f"♫   {display_name}", font=("Segoe UI", 12), text_color=theme.color("text"), anchor="w")
            name_label.pack(side="left", fill="x", expand=True, padx=10, pady=7)

            remove_button = ctk.CTkButton(
                row_frame, text="Remove", width=60, height=27, corner_radius=8,
                fg_color=theme.color("accent_bg"), hover_color=theme.color("border"),
                text_color=theme.color("accent_text"), font=("Segoe UI", 12, "bold"),
                command=lambda p=path: self.remove_file(p),
            )
            remove_button.pack(side="right", padx=6, pady=4)

            self.file_rows.append({"frame": row_frame, "name": name_label, "remove": remove_button})

        self.count_var.set(f"{len(self.selected_files)} " + ("file" if len(self.selected_files) == 1 else "files"))

    def remove_file(self, path):
        if path in self.selected_files:
            self.selected_files.remove(path)
        self.refresh_list()

    def apply_theme(self):
        self.card.configure(fg_color=theme.color("surface"), border_color=theme.color("border"))
        self.btn_choose.configure(fg_color=theme.color("primary"), hover_color=theme.color("primary_hover"))
        
        # Ustawiamy domyślne tło dla pola URL
        self.entry_url.configure(fg_color=theme.color("surface_alt"), border_color=theme.color("border"))
        
        if self.url_var.get() == "Paste YouTube link...":
            self.entry_url.configure(text_color=theme.color("muted"))
        else:
            self.entry_url.configure(text_color=theme.color("text"))
            
        self.btn_add_url.configure(fg_color=theme.color("accent_bg"), hover_color=theme.color("border"), text_color=theme.color("accent_text"))
        self.list_frame.configure(fg_color=theme.color("log_bg"), border_color=theme.color("border"))
        self.refresh_list()