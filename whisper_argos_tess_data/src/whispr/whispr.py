#!/usr/bin/env python3
import os
import threading
import traceback
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.scrolledtext import ScrolledText

import extractors
import translation
from file_utilities import FileFormats


def append(widget, text):
    def _append():
        widget.configure(state="normal")
        widget.insert("end", str(text) + "\n")
        widget.see("end")
        widget.configure(state="disabled")

    widget.after(0, _append)


def clear(widget):
    def _clear():
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.configure(state="disabled")

    widget.after(0, _clear)


def set_busy(is_busy, message=None):
    def _set():
        if is_busy:
            run_button.configure(state="disabled")
            progress_bar.start(12)
            progress_label_var.set(message or "Processing...")
        else:
            progress_bar.stop()
            progress_label_var.set(message or "Idle")
            run_button.configure(state="normal")

    root.after(0, _set)


def run_single_file():
    set_busy(True, "Processing selected file...")

    try:
        clear(output)

        path = input_file_var.get()
        outdir = output_dir_var.get() if write_output_var.get() else None
        source_lang = language_var.get()
        fmt_label = format_var.get()

        if not path or not os.path.exists(path):
            append(status, f"Input file does not exist: {path}")
            return

        selected_format = FileFormats.AUTO
        for f in FileFormats:
            if f.value == fmt_label:
                selected_format = f
                break

        append(status, f"Processing: {path}")

        result = extractors.extract_file(
            path,
            output_folder=outdir,
            file_format=selected_format,
            extract_attachments=extract_attachments_var.get(),
            process_attachments=process_attachments_var.get(),
            ocr=ocr_var.get(),
            from_lang=source_lang,
        )

        append(output, "EXTRACTED TEXT")
        append(output, "-" * 80)
        append(output, result[0] if result else "")

        if translate_var.get():
            set_busy(True, "Translating extracted text...")
            append(status, "Translating extracted text...")

            translated = translation.translate_text(
                result,
                source_lang,
                outdir,
                os.path.basename(path) + ".argos-translated.txt",
            )

            append(output, "\nTRANSLATED TEXT")
            append(output, "-" * 80)
            append(output, translated)

        append(status, "Finished.")

    except Exception:
        append(status, "UNEXPECTED ERROR:")
        append(status, traceback.format_exc())

    finally:
        set_busy(False, "Finished")


def run_single_file_thread():
    threading.Thread(target=run_single_file, daemon=True).start()


def choose_file():
    p = filedialog.askopenfilename()
    if p:
        input_file_var.set(p)


def choose_output_dir():
    p = filedialog.askdirectory()
    if p:
        output_dir_var.set(p)


def load_languages():
    langs = ["Auto", "Auto (Multi)"]
    try:
        import argostranslate.translate

        for lang in argostranslate.translate.get_installed_languages():
            for to_lang in lang.translations_to:
                if to_lang.code == "en":
                    langs.append(f"{lang.code} --- {lang.name}")

    except Exception as e:
        langs.append("Argos languages unavailable")
        append(status, f"Argos language load error: {e}")

    return langs


root = tk.Tk()
root.title("W.H.I.S.P.R. Linux Port")

input_file_var = tk.StringVar()
output_dir_var = tk.StringVar()
write_output_var = tk.BooleanVar(value=True)
ocr_var = tk.BooleanVar(value=True)
extract_attachments_var = tk.BooleanVar(value=False)
process_attachments_var = tk.BooleanVar(value=False)
translate_var = tk.BooleanVar(value=False)
language_var = tk.StringVar(value="Auto")
format_var = tk.StringVar(value=FileFormats.AUTO.value)
progress_label_var = tk.StringVar(value="Idle")

top = ttk.Frame(root, padding=10)
top.pack(fill="x")

ttk.Label(top, text="Input File:").grid(row=0, column=0, sticky="w")
ttk.Entry(top, textvariable=input_file_var, width=70).grid(row=0, column=1, sticky="ew")
ttk.Button(top, text="Browse", command=choose_file).grid(row=0, column=2)

ttk.Checkbutton(top, text="Write Output To Folder", variable=write_output_var).grid(row=1, column=0, sticky="w")
ttk.Entry(top, textvariable=output_dir_var, width=70).grid(row=1, column=1, sticky="ew")
ttk.Button(top, text="Select Output Dir", command=choose_output_dir).grid(row=1, column=2)

ttk.Checkbutton(top, text="Use OCR", variable=ocr_var).grid(row=2, column=0, sticky="w")
ttk.Checkbutton(top, text="Extract Attachments", variable=extract_attachments_var).grid(row=2, column=1, sticky="w")
ttk.Checkbutton(top, text="Process Attachments", variable=process_attachments_var).grid(row=2, column=2, sticky="w")

ttk.Checkbutton(top, text="Translate Extracted Text", variable=translate_var).grid(row=3, column=0, sticky="w")

ttk.Label(top, text="Source Language:").grid(row=4, column=0, sticky="w")
language_combo = ttk.Combobox(top, textvariable=language_var, values=["Auto", "Auto (Multi)"], width=30)
language_combo.grid(row=4, column=1, sticky="w")

ttk.Label(top, text="File Type:").grid(row=5, column=0, sticky="w")
format_combo = ttk.Combobox(top, textvariable=format_var, values=[f.value for f in FileFormats], width=40)
format_combo.grid(row=5, column=1, sticky="w")

run_button = ttk.Button(top, text="Run For Selected File", command=run_single_file_thread)
run_button.grid(row=6, column=1, pady=8, sticky="w")

ttk.Label(top, textvariable=progress_label_var).grid(row=7, column=0, sticky="w")
progress_bar = ttk.Progressbar(top, mode="indeterminate", length=420)
progress_bar.grid(row=7, column=1, columnspan=2, sticky="ew", pady=(2, 8))

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

output = ScrolledText(tabs, wrap="word", state="disabled")
status = ScrolledText(tabs, wrap="word", state="disabled")

tabs.add(output, text="Output")
tabs.add(status, text="Status")

try:
    language_combo["values"] = load_languages()
except Exception:
    pass

try:
    extractors.external_dependencies_check()
except Exception as e:
    append(status, f"Dependency check error: {e}")

root.mainloop()
