# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_all

# 1. Zbieranie domyślnych plików faster_whisper i customtkinter
datas, binaries, hiddenimports = collect_all('faster_whisper')
datas += collect_all('customtkinter')[0]

# 2. Dodawanie ikony
datas += [('purple_pen.ico', '.')]

# 3. Wstrzykiwanie bibliotek CUDA prosto do ctranslate2
site_packages = Path(r"C:\Users\blaze\AppData\Local\Programs\Python\Python312\Lib\site-packages")
extra_binaries = [
    (str(site_packages / "nvidia" / "cublas" / "bin" / "cublas64_12.dll"), "ctranslate2"),
    (str(site_packages / "nvidia" / "cublas" / "bin" / "cublasLt64_12.dll"), "ctranslate2"),
    (str(site_packages / "nvidia" / "cuda_runtime" / "bin" / "cudart64_12.dll"), "ctranslate2"),
]
binaries += extra_binaries

# 4. Analiza
a = Analysis(
    ['main.py'], 
    pathex=[], 
    binaries=binaries, 
    datas=datas, 
    hiddenimports=hiddenimports + ['yt_dlp', 'yt_dlp.compat', 'tkinter', 'docx'], 
    hookspath=[], 
    hooksconfig={}, 
    runtime_hooks=[], 
    excludes=[], 
    noarchive=False
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WHISPERER_V1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='purple_pen.ico'
)