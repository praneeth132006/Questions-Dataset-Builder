import pdfplumber
import pandas as pd
import re
import os

PDF_PATH = "paper 1.pdf"   # <-- your PDF file
CSV_OUT = "upsc_prelims_questions.csv"
JSON_OUT = "upsc_prelims_questions.json"

# ---------------- SUBJECT CLASSIFICATION ----------------
def classify_subject(text):
    t = text.lower()
    if any(k in t for k in ["constitution", "parliament", "panchayat", "fundamental", "president"]):
        return "Polity"
    if any(k in t for k in ["gdp", "inflation", "budget", "bank", "economy", "fiscal"]):
        return "Economy"
    if any(k in t for k in ["biodiversity", "ecosystem", "climate", "carbon", "environment"]):
        return "Environment & Ecology"
    if any(k in t for k in ["river", "monsoon", "plateau", "latitude", "ocean"]):
        return "Geography"
    if any(k in t for k in ["vedic", "gandhi", "congress", "british", "freedom"]):
        return "History"
    if any(k in t for k in ["satellite", "nuclear", "biotechnology", "dna", "reactor"]):
        return "Science & Technology"
    return "General Studies"

# ---------------- DIFFICULTY TAGGING ----------------
def tag_difficulty(text):
    if text.count(";") >= 2 or "which of the following statements" in text.lower():
        return "Hard"
    if "consider the following" in text.lower():
        return "Medium"
    return "Easy"

# ---------------- PDF EXTRACTION ----------------
if not os.path.exists(PDF_PATH):
    print(f"❌ Error: File '{PDF_PATH}' not found!")
    print(f"   Current directory: {os.getcwd()}")
    print(f"   Please ensure the PDF file is in the correct location.")
    exit(1)

raw_text = ""
with pdfplumber.open(PDF_PATH) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            raw_text += page_text + "\n"

# ---------------- QUESTION PARSING ----------------
# More flexible pattern to handle various formats
pattern = re.compile(
    r"(\d+)\.\s*(.*?)"                           # Question number and text
    r"\s*\(a\)\s*(.*?)"                          # Option A
    r"\s*\(b\)\s*(.*?)"                          # Option B
    r"\s*\(c\)\s*(.*?)"                          # Option C
    r"\s*\(d\)\s*(.*?)"                          # Option D
    r"\s*(?:Answer[:\-\s]*|Ans[:\-\s]*)\s*\(?([A-Da-d])\)?",  # Answer in various formats
    re.S | re.I
)

questions = []

for match in pattern.finditer(raw_text):
    qid, q, a, b, c, d, ans = match.groups()
    questions.append({
        "question_id": int(qid),
        "question": " ".join(q.split()),
        "option_A": " ".join(a.split()),
        "option_B": " ".join(b.split()),
        "option_C": " ".join(c.split()),
        "option_D": " ".join(d.split()),
        "correct_option": ans.upper(),
        "difficulty": tag_difficulty(q),
        "subject": classify_subject(q)
    })

# ---------------- EXPORT ----------------
if not questions:
    print("⚠️ No questions were extracted. The PDF format might not match the expected pattern.")
    print("   First 500 characters of extracted text:")
    print(raw_text[:500] if raw_text else "(No text extracted)")
    exit(1)

df = pd.DataFrame(questions)
df.sort_values("question_id", inplace=True)

df.to_csv(CSV_OUT, index=False)
df.to_json(JSON_OUT, orient="records", indent=2, force_ascii=False)

print(f"✅ Extracted {len(df)} questions")
print(f"📁 CSV saved as {CSV_OUT}")
print(f"📁 JSON saved as {JSON_OUT}")
