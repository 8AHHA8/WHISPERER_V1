import customtkinter as ctk
from assets.config import C

class ThemeManager:
    def __init__(self):
        self.mode = "dark"

    def toggle(self):
        self.mode = "dark" if self.mode == "light" else "light"
        ctk.set_appearance_mode(self.mode)
        return self.mode

    def color(self, key):
        index = 1 if self.mode == "dark" else 0
        return C[key][index]

theme = ThemeManager()