# W.H.I.S.P.R. Python

Cross-platform Python rebuild of the W.H.I.S.P.R. GUI.

This repository tracks editable source code only.

Large runtime assets are intentionally excluded from Git:
- Whisper / Faster-Whisper models
- Tesseract data
- Windows installers
- extracted PyInstaller artifacts
- generated transcripts and outputs

Expected optional local payload folder:
- whisper_files/Faster-Whisper-XXL/

Current supported features:
- GUI file selection
- progress bar
- TXT extraction
- PDF extraction
- DOCX/PPTX extraction
- image OCR via Tesseract
- HTML/RTF extraction
- basic EML/MBOX parsing
- Argos translation when language packages are installed

Work in progress:
- Windows path detection
- Faster-Whisper audio/video transcription
- PST/OST extraction
