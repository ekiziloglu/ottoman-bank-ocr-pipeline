# Ottoman Bank Archive — OCR & LLM Data Extraction Pipeline

An end-to-end pipeline for digitizing handwritten Ottoman Bank personnel records from archival JPG documents, combining **Google Cloud Vision API** for OCR and **Gemini 1.5 Pro** for translation and structuring of historical French text into clean, analysis-ready English output.

> Research Project — Sabancı University  
> Supervisor: **Selim Balcısoy**  
> Data: Provided exclusively by **SALT Galata** for academic use (not included in this repository)

---

## Problem

The Ottoman Bank archive contains thousands of handwritten personnel records (1855–1926), written in old French on scanned JPG documents. Manual transcription and translation of these records is prohibitively time-consuming. This project builds an automated pipeline that:

1. Extracts handwritten text from archival images
2. Translates and structures the French content into modern English
3. Prepares the output for downstream analytics (used in the companion [Ottoman Bank Historical Dashboard](https://github.com/ekiziloglu) project)

## Pipeline Architecture

​```
   ┌──────────────────┐
   │ Archival JPG     │  Handwritten French personnel record
   │ (1855–1926)      │
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │ Google Cloud     │  OCR → raw extracted French text
   │ Vision API       │
   └────────┬─────────┘
            │
            ▼
   ┌──────────────────┐
   │ Gemini 1.5 Pro   │  Translation + structuring →
   │                  │  clean professional English
   └────────┬─────────┘  (preserves names, dates, monetary values)
            │
            ▼
   ┌──────────────────┐
   │ Structured Data  │  Normalized records → pandas/xlsxwriter
   │ (downstream)     │  → tabular Excel reports
   └──────────────────┘
​```

## Tech Stack

`Python 3` · `Google Cloud Vision API` · `Gemini 1.5 Pro` · `google-generativeai` · `pandas` · `xlsxwriter`

## Repository Contents

- `ottoman_ocr_pipeline.py` — Core pipeline: OCR + LLM translation
- `.env.example` — Template for required environment variables
- `requirements.txt` — Python dependencies
- `.gitignore` — Excludes credentials and archival data

## Setup

### 1. Install dependencies

​```bash
pip install -r requirements.txt
​```

### 2. Configure credentials

You need credentials for two Google services:

**Google Cloud Vision API:**
- Create a Google Cloud project and enable the Vision API
- Create a service account and download its JSON key
- Save the JSON file somewhere safe (outside the repo)

**Gemini API:**
- Get a key from [Google AI Studio](https://aistudio.google.com/app/apikey)

Create a `.env` file (copy from `.env.example`):

​```env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account.json
GEMINI_API_KEY=your-gemini-api-key
​```

Then export the variables before running:

​```bash
export $(cat .env | xargs)
​```

### 3. Run the pipeline

​```bash
python ottoman_ocr_pipeline.py
​```

The script processes an archival image, runs OCR via Vision API, and pipes the extracted text through Gemini for translation and cleanup.

## Key Concepts Demonstrated

- Cloud-based OCR for handwritten historical documents
- LLM-driven translation with domain-specific prompting (handwritten old French → modern English)
- Structured pipeline design for transforming unstructured archival data into analysis-ready datasets
- Secure credential handling via environment variables
- Integration of multiple Google Cloud / AI services into a unified workflow

## Data Availability

The archival JPG images and extracted personnel records are **not included** in this repository, as the data was provided by SALT Galata exclusively for academic use. Researchers interested in similar archival data should contact [SALT Galata](https://saltonline.org/en/) directly.

## Companion Project

The structured output from this pipeline is consumed by the **Ottoman Bank Historical Dashboard** — an interactive Dash/Plotly analytics tool exploring career trajectories of 6,000+ Ottoman Bank employees (1855–1926).
