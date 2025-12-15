import os
from spellchecker import SpellChecker
from fuzzywuzzy import process

VIDEO_FOLDER = "static/videos"
spell = SpellChecker()

def correct_spelling(text):
    """
    Splits text into words, checks spelling for each, 
    and returns the corrected phrase.
    """
    if not text:
        return ""
    
    # Split sentence into individual words
    words = text.split()
    corrected_words = []

    for word in words:
        # Get correction. If correction is None, keep original word.
        correction = spell.correction(word)
        if correction:
            corrected_words.append(correction)
        else:
            corrected_words.append(word)
            
    return " ".join(corrected_words)

def get_best_video_match(text):
    """Return best matching video using fuzzy matching."""
    if not text:
        return None

    try:
        files = os.listdir(VIDEO_FOLDER)
        # remove extensions for matching
        video_names = [f.replace(".mp4", "") for f in files if f.endswith(".mp4")]

        if not video_names:
            return None

        # Extract best match
        match, score = process.extractOne(text, video_names)
        
        # Threshold (65 is okay, 75 is safer to avoid bad matches)
        if score >= 65:
            return match + ".mp4"
            
    except Exception as e:
        print(f"Matching error: {e}")
        
    return None