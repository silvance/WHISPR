import os
from enum import Enum


class FileFormats(Enum):
    AUTO = "Auto Detect"
    PPTX = "PowerPoint 2007+ (PPTX/PPTM)"
    PPT = "PowerPoint Pre-2007 (PPT)"
    DOCX = "Word 2007+ (DOCX/DOCM)"
    DOC = "Word Pre-2007 (DOC)"
    XLS = "Excel (XLS/XLSM/XLSX)"
    PDF = "Adobe Portable Document Format (PDF)"
    EML = "Electronic Mail Format (EML)"
    MBOX = "Email Message Collection (MBOX)"
    PST = "Storage Table (MS Outlook - PST/OST)"
    TXT = "Text File (TXT)"
    RTF = "Rich Text Format (RTF)"
    HTML = "Hypertext Markup Language (HTML/HTM)"
    IMAGE = "Image File (Supported by PIL)"
    AV = "Audio/Visual File (Supported by FFMPEG)"


def get_nonexistant_path(path):
    if not os.path.exists(path):
        return path

    root, ext = os.path.splitext(path)
    i = 1
    while True:
        candidate = f"{root}_{i}{ext}"
        if not os.path.exists(candidate):
            return candidate
        i += 1


def get_files_recursively(folder):
    files = []
    for root, _, names in os.walk(folder):
        for name in names:
            files.append(os.path.join(root, name))
    return files


def write_pdf_from_txt_file(txt_path, pdf_path=None):
    # Placeholder for original WHISPR compatibility.
    # Linux port writes text files for now.
    return None
