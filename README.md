# WHISPERER_V1

WHISPERER_V1 is a desktop application designed for fast and accurate audio transcription. Powered by the Faster-Whisper engine, it processes local audio files and YouTube links, generating structured Microsoft Word (`.docx`) documents with precise word-level timestamps.

The application features a modern graphical interface built with CustomTkinter, offering light and dark themes, real-time progress tracking, and detailed logging.

## Features

### Audio Transcription and Processing

- **Multi-source input** — Transcribe local audio files or provide YouTube links for automatic download and processing.
- **Supported audio formats** — `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`, `.aac`, and `.wma`.
- **High-performance engine** — Uses `faster-whisper` with the `large-v3-turbo` model.
- **GPU acceleration** — Supports NVIDIA GPU acceleration through CUDA and CTranslate2.
- **Word-level timestamps** — Generates transcripts with precise word timing.
- **Structured output** — Saves transcriptions as formatted `.docx` documents with automatic `[X min]` navigation markers.
- **Auto-save functionality** — Periodically saves transcription progress to reduce the risk of data loss during long recordings.

### Modern Graphical Interface

- **Modern interface** — Built with `customtkinter`.
- **Theme switching** — Switch between light and dark modes.
- **Real-time progress** — Progress bars and percentage indicators for transcription tasks.
- **Detailed logging** — Displays timestamps, status messages, warnings, and errors.
- **File management** — Add and remove audio files and YouTube links from the processing queue.

## Requirements

### Software

- **Python:** 3.10–3.12.
- **Git:** Required to clone the repository.
- **FFmpeg:** Required for audio processing.
- **NVIDIA GPU:** Optional, recommended for accelerated transcription.
- **CUDA-compatible libraries:** Required for NVIDIA GPU acceleration.

Python package dependencies are listed in `requirements.txt`.

The first launch may download the Whisper model and its required files. An internet connection and additional disk space may therefore be necessary.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/8AHHA8/WHISPERER_V1.git
cd WHISPERER_V1
```

### 2. Create a Virtual Environment

**Windows:**

```bat
python -m venv venv
```

**Linux:**

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**Windows — Command Prompt:**

```bat
venv\Scripts\activate.bat
```

**Windows — PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, review your execution policy before changing it.

**Linux:**

```bash
source venv/bin/activate
```

Using a virtual environment helps isolate project dependencies from other Python installations.

### 4. Install System Dependencies

**Windows**

Install Git and FFmpeg if they are not already available. Make sure FFmpeg is added to the system `PATH`.

**Linux — Ubuntu / Debian**

```bash
sudo apt update
sudo apt install python3-tk ffmpeg
```

Package names may differ on other Linux distributions.

### 5. Install Python Dependencies

Upgrade pip and install the project dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The `av` library is pinned below version `19.0.0` to avoid compatibility issues with the Faster-Whisper engine.

### 6. Configure CUDA (Optional)

WHISPERER_V1 supports NVIDIA GPU acceleration through CTranslate2.

The application adds NVIDIA DLL directories from the virtual environment to the Windows DLL search path.

To check whether CTranslate2 detects a CUDA-compatible GPU, run:

```bash
python -c "import ctranslate2; print('CUDA devices:', ctranslate2.get_cuda_device_count())"
```

If the result is `1` or higher, CTranslate2 detects at least one CUDA device. If the result is `0`, no CUDA device is detected.

**Note:** A result of `0` does not automatically mean that the application switches to CPU mode. CPU execution requires configuring `DEVICE = "cpu"` in `config.py`, unless automatic fallback has been implemented separately.

If necessary, install the NVIDIA CUDA libraries:

```bash
python -m pip install nvidia-cublas-cu12 nvidia-cudnn-cu12
```

### 7. Run the Application

Start WHISPERER_V1 from the project directory:

```bash
python main.py
```

On the first launch, the application may download the required Whisper model files. Startup time depends on your internet connection and available hardware.

## Usage

The general workflow is:

1. Launch WHISPERER_V1.
2. Add one or more audio files or paste YouTube links into the input field.
3. Select the output folder where the `.docx` files will be saved.
4. Click **Start Transcription**.
5. Monitor progress using the progress bar and log window.
6. Access the resulting Word documents in the selected output folder.

## Project Structure

The repository currently uses the following structure:

```text
WHISPERER_V1/
├── .vscode/
├── .gitignore
├── WHISPERER.spec
├── config.py
├── core_audio.py
├── core_docx.py
├── main.py
├── purple_pen.ico
├── theme_manager.py
├── ui_files_section.py
└── ui_progress_section.py
```

## Output Format

Generated transcripts are saved as Microsoft Word (`.docx`) documents in the user-selected output folder.

The documents:

- Use the **Aptos** font.
- Include word-level transcription timestamps.
- Contain automatic `[X min]` markers to facilitate navigation through longer recordings.

## Troubleshooting

### FFmpeg Is Not Recognized

If the terminal reports that FFmpeg is not recognized, verify that it is installed and that its executable directory is included in the system `PATH`.

```bash
ffmpeg -version
```

### PyAV TypeError on Audio Loading

If you encounter an error similar to:

```text
open() got an unexpected keyword argument 'metadata_errors'
```

install a compatible version of PyAV:

```bash
python -m pip install "av<19"
```

### CUDA or GPU Errors

If transcription is slow or errors related to CUDA appear:

- Update your NVIDIA drivers.
- Verify that CTranslate2 detects your GPU.
- Check that the required NVIDIA CUDA libraries are installed.
- Verify the `DEVICE` and `COMPUTE_TYPE` settings in `config.py`.

If GPU execution is unavailable, change:

```python
DEVICE = "cpu"
```

CPU transcription may be significantly slower.

### Model Download or Loading Errors

Check your internet connection, available disk space, and access to the Hugging Face model repository. Ensure that your firewall or antivirus software is not blocking model downloads.

### YouTube Download Errors

Make sure `yt-dlp` is up to date:

```bash
python -m pip install --upgrade yt-dlp
```

## License and Responsible Use

WHISPERER_V1 uses third-party libraries and AI models, including Faster-Whisper and OpenAI Whisper models.

Ensure that you have the necessary rights and permissions to download and transcribe audio content, particularly material obtained from YouTube and other third-party platforms.

## Author

**GitHub Repository:**

https://github.com/8AHHA8/WHISPERER_V1