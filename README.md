# UPSC Prelims PDF to CSV/JSON Converter

## Overview

This Python script extracts multiple-choice questions from UPSC Prelims PDF papers and converts them into structured CSV and JSON formats. It automatically:

- Parses question text and all four options (A, B, C, D)
- Extracts the correct answer
- Classifies questions by subject (Polity, Economy, History, etc.)
- Tags difficulty level (Easy, Medium, Hard)

## Output Format

Each extracted question contains:
| Field | Description |
|-------|-------------|
| `question_id` | Question number from the PDF |
| `question` | The question text |
| `option_A` to `option_D` | The four answer choices |
| `correct_option` | The correct answer (A/B/C/D) |
| `difficulty` | Easy, Medium, or Hard |
| `subject` | Classified subject area |

## Installation

### Step 1: Navigate to the project directory

```bash
cd /Users/praneeth/Downloads/demo
```

### Step 2: (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
# OR
venv\Scripts\activate      # On Windows
```

### Step 3: Install required libraries

Install all dependencies at once:

```bash
pip install -r requirements.txt
```

Or install them individually:

```bash
pip install pdfplumber
pip install pandas
```

### Step 4: Verify installation

```bash
pip list
```

You should see `pdfplumber` and `pandas` in the list.

## Configuration

### Changing the Input PDF File

Open `upsc_pdf_to_csv_json.py` and modify **line 7**:

```python
PDF_PATH = "paper 1.pdf"   # <-- Change this to your PDF filename
```

### Changing Output File Names

Modify **lines 8-9** to change output filenames:

```python
CSV_OUT = "upsc_prelims_questions.csv"   # <-- Change CSV output name
JSON_OUT = "upsc_prelims_questions.json"  # <-- Change JSON output name
```

## Usage

1. Place your PDF file in the same directory as the script
2. Update the `PDF_PATH` variable (line 7) with your PDF filename
3. Run the script:

```bash
python upsc_pdf_to_csv_json.py
```

4. Find your output files in the same directory

## Complete Terminal Commands Summary

```bash
# Navigate to project folder
cd /Users/praneeth/Downloads/demo

# Install dependencies
pip install -r requirements.txt

# Run the script
python upsc_pdf_to_csv_json.py
```

## Expected PDF Format

The script expects questions in this format:

```
1. Question text here?
(a) Option A text
(b) Option B text
(c) Option C text
(d) Option D text
Answer:- A
```

## Troubleshooting

- **"File not found" error**: Ensure the PDF is in the same directory and the filename matches exactly
- **"No questions extracted"**: Your PDF format may differ from the expected pattern. Check the debug output showing the first 500 characters of extracted text.
- **"ModuleNotFoundError"**: Run `pip install -r requirements.txt` to install missing libraries
- **"pip not found"**: Use `pip3` instead of `pip`, or ensure Python is properly installed
