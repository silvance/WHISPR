import os

from file_utilities import get_nonexistant_path


def _write_if_requested(text, output_folder=None, translated_basename=None):
    if output_folder and translated_basename and os.path.isdir(output_folder):
        out = get_nonexistant_path(os.path.join(output_folder, translated_basename))
        with open(out, "w", encoding="utf-8", errors="replace") as f:
            f.write(text or "")
        print(f"Wrote translated text to {out}")
    return text or ""


def _get_translation(from_code, to_code="en"):
    import argostranslate.translate

    installed = argostranslate.translate.get_installed_languages()
    from_lang = next((l for l in installed if l.code == from_code), None)
    to_lang = next((l for l in installed if l.code == to_code), None)

    if not from_lang or not to_lang:
        return None

    return from_lang.get_translation(to_lang)


def translate_single_language(text, from_code, output_folder=None, translated_basename=None, write_to_pdf=False):
    text = text or ""
    try:
        trans = _get_translation(from_code, "en")
        if not trans:
            result = f"[No installed Argos translation from {from_code} to en]\n\n{text}"
        else:
            result = trans.translate(text)
    except Exception as e:
        result = f"[Translation error: {e}]\n\n{text}"

    return _write_if_requested(result, output_folder, translated_basename)


def auto_translate_single_language(text, output_folder=None, translated_basename=None, write_to_pdf=False):
    # Simple fallback: try Spanish/French/German/Russian/Arabic/Persian/Pashto/Dari-style common codes.
    # Exact auto-detection can be added later with lingua.
    text = text or ""

    for code in ("es", "fr", "de", "ru", "ar", "fa", "ps", "pt", "it", "zh"):
        trans = _get_translation(code, "en")
        if trans:
            try:
                result = trans.translate(text)
                return _write_if_requested(result, output_folder, translated_basename)
            except Exception:
                pass

    return _write_if_requested("[No usable Argos auto-translation pair installed]\n\n" + text, output_folder, translated_basename)


def auto_translate_multi_languages(text, output_folder=None, translated_basename=None, write_to_pdf=False):
    return auto_translate_single_language(text, output_folder, translated_basename, write_to_pdf)


def translate_text(result, from_lang="Auto", output_folder=None, translated_basename=None, write_to_pdf=False):
    text = ""

    if isinstance(result, list) and result:
        text = result[0] or ""
    elif isinstance(result, str):
        text = result

    if not translated_basename:
        translated_basename = "argos-translated.txt"

    if from_lang == "Auto":
        return auto_translate_single_language(text, output_folder, translated_basename, write_to_pdf)

    if from_lang == "Auto (Multi)":
        return auto_translate_multi_languages(text, output_folder, translated_basename, write_to_pdf)

    from_code = from_lang.split(" --- ")[0].strip()
    return translate_single_language(text, from_code, output_folder, translated_basename, write_to_pdf)
