import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from langdetect import detect
from ..config import LANGUAGE_CODES

load_dotenv()
API = os.getenv('DETECT_LANG_API')

async def translate_text(text: str, dest_lang: str) -> dict:
    """
    Translate text to the specified language.
    
    Args:
        text (str): Text to translate
        dest_lang (str): Destination language code
        
    Returns:
        dict: Dictionary containing translated text and source language
    """
    try:
        # First detect the source language
        src_lang = await detect_language(text)
        
        # Initialize translator with detected source language
        translator = GoogleTranslator(source=src_lang, target=dest_lang)
        
        # Perform translation
        translated_text = translator.translate(text)
        
        return {
            'text': translated_text,
            'src': src_lang
        }
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")

async def detect_language(text: str) -> str:
    """
    Detect the language of the given text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        str: Detected language code
    """
    try:
        detected = detect(text)
        return detected
    except Exception as e:
        raise Exception(f"Language detection failed: {str(e)}")

def get_language_name(language_code: str) -> str:
    """
    Get the full name of a language from its code.
    
    Args:
        language_code (str): Language code
        
    Returns:
        str: Full language name
    """
    return LANGUAGE_CODES.get(language_code, 'Unknown') 