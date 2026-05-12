"""
Ottoman Bank Archive OCR & LLM Pipeline
----------------------------------------
Extracts handwritten French text from archival JPG images using Google Cloud
Vision API, then uses Gemini 1.5 Pro to translate and clean the text into
structured English output.

Setup:
    1. Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point
       to your Google Cloud service account JSON file:
           export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

    2. Set the GEMINI_API_KEY environment variable with your Gemini API key:
           export GEMINI_API_KEY="your-key-here"

    Alternatively, create a .env file (see .env.example) and use python-dotenv.
"""

import os
import logging
import absl.logging

# Suppress gRPC and absl logging noise
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""
logging.root.removeHandler(absl.logging._absl_handler)
absl.logging._warn_preinit_stderr = False

from google.cloud import vision
import google.generativeai as genai


# ---------------------------------------------------------------------------
# Configuration — read from environment variables (never hardcode credentials)
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError(
        "GEMINI_API_KEY environment variable is not set. "
        "Set it before running the script."
    )

# Google Cloud Vision uses GOOGLE_APPLICATION_CREDENTIALS automatically
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    raise EnvironmentError(
        "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set. "
        "Point it to your Google Cloud service account JSON file."
    )

genai.configure(api_key=GEMINI_API_KEY)
client = vision.ImageAnnotatorClient()


# ---------------------------------------------------------------------------
# OCR: Extract text from archival image using Google Cloud Vision
# ---------------------------------------------------------------------------
def detect_text(image_path: str) -> str:
    """Run OCR on an image file and return the extracted text."""
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        print("Detected Text:")
        print(texts[0].description)
        return texts[0].description

    print("No text found in the image.")
    return ""


# ---------------------------------------------------------------------------
# LLM: Translate and structure historical French text using Gemini 1.5 Pro
# ---------------------------------------------------------------------------
def translate_and_clean_text_with_gemini(text: str) -> str:
    """Translate handwritten historical French OCR output into clean English."""
    print("\nTranslating and cleaning the text into English...")
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = (
        "You are an expert translator who translates old French handwritten "
        "documents into modern English. Translate the text into clear, "
        "professional English, preserving dates, proper names, and monetary "
        "values. Make the text readable and well-organized into proper "
        f"paragraphs without changing its meaning.\n\n{text}"
    )

    response = model.generate_content(prompt)
    return response.text


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Path to the archival document image to process.
    # Replace with the path to your own image, or read from sys.argv / config.
    test_image = "sample_data/example_record.jpg"

    extracted_text = detect_text(test_image)

    if extracted_text:
        cleaned_text = translate_and_clean_text_with_gemini(extracted_text)
        print("\nTranslated and Cleaned Text (English):")
        print(cleaned_text)
    else:
        print("No text was detected.")
