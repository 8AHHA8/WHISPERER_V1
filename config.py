# config.py
MODEL_NAME = "large-v3-turbo"
DEVICE = "cuda"
COMPUTE_TYPE = "int8_float16"

AUDIO_TYPES = [
    ("Audio Files", "*.mp3 *.wav *.m4a *.flac *.ogg *.aac *.wma"),
    ("All Files", "*.*"),
]

C = {
    "bg":             ("#F4F6F9", "#0E0C13"),
    "surface":        ("#FFFFFF", "#17151F"),
    "surface_alt":    ("#F0F2F6", "#23202E"),
    "surface_hover":  ("#E2E6ED", "#302C3E"),
    "border":         ("#D1D5DB", "#302C3E"),
    "text":           ("#000000", "#FFFFFF"), # <-- ZMIENIONO NA CZYSTĄ CZERŃ I BIEL
    "muted":          ("#6B7280", "#9CA3AF"),
    "primary":        ("#6366F1", "#8B5CF6"),
    "primary_hover":  ("#4F46E5", "#7C3AED"),
    "accent_bg":      ("#E0E7FF", "#2E2545"),
    "accent_text":    ("#4338CA", "#C4B5FD"),
    "danger":         ("#EF4444", "#F87171"),
    "log_bg":         ("#F9FAFB", "#12101A"),
    "warning":        ("#F59E0B", "#FBBF24"),
    "progress_bg":    ("#E5E7EB", "#2D283A"),
    "frame_hover":    ("#F9FAFB", "#1C1925"),
}