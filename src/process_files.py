from io import BytesIO
import os

from docx_processing import DocxTranslator
from translation import detect_language, translate_text


class UnsuportedFileFormatError(Exception):
    """
    Exception raised when the file format is not supported
    """
    pass


def process_txt_file(file, target_language):
    """
    Process a .txt file and return the translated file and the source language
    
    Args:
        file (werkzeug.datastructures.FileStorage): The file to process
        target_language (str): The language code of the target language

    Returns:
        tuple: A tuple containing the translated file and the source language
    """
    # Read the file content
    file_content = file.read().decode('utf-8')
    # Translate the text
    source_language = detect_language(file_content)
    translated_text = translate_text(file_content, source_language, target_language)
    # Create an in-memory file with the translated text
    translated_file = BytesIO()
    translated_file.write(translated_text.encode('utf-8'))
    translated_file.seek(0)
    return translated_file, source_language

def process_docx_file(file, target_language):
    """
    Process a .docx file and return the translated file and the source language

    Args:
        file (werkzeug.datastructures.FileStorage): The file to process
        target_language (str): The language code of the target language

    Returns:
        tuple: A tuple containing the translated file and the source language
    """
    docx_translator = DocxTranslator(file, target_language)
    translated_doc = docx_translator.process_document()
    translated_file = BytesIO()
    translated_doc.save(translated_file)
    translated_file.seek(0)
    return translated_file, docx_translator.detected_language

def process_file(file, target_language):
    """
    Process a file and return the translated file and the source language

    Args:
        file (werkzeug.datastructures.FileStorage): The file to process
        target_language (str): The language code of the target language

    Returns:
        tuple: A tuple containing the translated file and the source language

    Raises:
        UnsuportedFileFormatError: If the file format is not supported
    """
    file_ext = os.path.splitext(file.filename)[1].lower()  # Get file extension
    if file_ext == ".txt":
        return process_txt_file(file, target_language)
    elif file_ext == ".docx":
        return process_docx_file(file, target_language)
    else:
        raise UnsuportedFileFormatError("Unsupported file format (only .txt files are supported)")
