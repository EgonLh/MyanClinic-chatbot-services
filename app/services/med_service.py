"""
Service for medicine identifier.
Uses OCR + medicine database lookup (with optional fuzzy matching).
"""

import io
import json
from PIL import Image
from pathlib import Path as PPath
import pytesseract
from rapidfuzz import fuzz
import re
# Load medicine database from JSON file
try:
    BASE_DIR = PPath(__file__).resolve().parent.parent
    print(BASE_DIR)
    JSONDIR = BASE_DIR / "data" / "main_db" / "medicine.json"
    with open(JSONDIR, "r", encoding="utf-8") as f:
        MEDICINE_DB = json.load(f)
    print("Pass")
except FileNotFoundError:
    print("Error >> ")
    # fallback if JSON doesn't exist
    MEDICINE_DB = [
        {
            "Medicine Name": "Paracetamol",
            "Composition": "Paracetamol 500mg",
            "Uses": "Pain relief, fever reduction",
            "Side_effects": "Nausea, rash",
            "Image URL": "",
            "Manufacturer": "ABC Pharma",
            "Excellent Review %": 0,
            "Average Review %": 0,
            "Poor Review %": 0,
        },
        {
            "Medicine Name": "Ibuprofen",
            "Composition": "Ibuprofen 400mg",
            "Uses": "Pain, inflammation, fever",
            "Side_effects": "Stomach pain, dizziness",
            "Image URL": "",
            "Manufacturer": "XYZ Pharma",
            "Excellent Review %": 0,
            "Average Review %": 0,
            "Poor Review %": 0,
        },
    ]

def identify_medicine(image_bytes: bytes, threshold: int = 80) -> dict:
    """
    Identify medicine from an image.

    Returns all required fields to match MedicineResponse.
    """
    # Default "Unknown" record
    unknown = {
        "Medicine Name": "Unknown",
        "Composition": "",
        "Uses": "",
        "Side_effects": "",
        "Image URL": "",
        "Manufacturer": "",
        "Excellent Review %": 0,
        "Average Review %": 0,
        "Poor Review %": 0,
    }

    try:
        image = Image.open(io.BytesIO(image_bytes))
    except Exception:
        return unknown

    # OCR text
    text = pytesseract.image_to_string(image, config="--psm 6").lower()
    text = text.replace("\n", " ").replace("\t", " ")
    text = re.sub(r"[^a-z\s]", "", text.lower())
    exclude_words = {"only", "vaccine"}

    # Split and filter
    words = [w.strip() for w in text.split() if len(w.strip()) > 3 and w.strip() not in exclude_words]

    print(words)
    
    if "avastin" in  ("Avastin 400mg Injection").lower():
        print("Hello")
    # Check each medicine
    for med in MEDICINE_DB:
        med_name_words = med["Medicine Name"].lower()
        # Check if all words in medicine name appear in OCR text words
        for word in words:
            # print("word :",word)
            # print("data :",med_name_words)
            if(word in med_name_words):
                # print("pass")
                return med
        


    # Fuzzy match
    best_match = None
    best_score = 0
    for med in MEDICINE_DB:
        score = fuzz.partial_ratio(med["Medicine Name"].lower(), text)
        if score > best_score:
            best_score = score
            best_match = med

    if best_score >= threshold and best_match:
        return best_match

    # No match
    return unknown

