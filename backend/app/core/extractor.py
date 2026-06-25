import re

PATTERNS = {
    "emails": r"[\w.\-]+@[\w\-]+\.[\w.\-]+",
    "dates": r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
             r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s*\d{4})\b",
    "money": r"(?:[$₹€£]\s?\d[\d,]*(?:\.\d+)?)|(?:\d[\d,]*\s?(?:USD|INR|EUR))",
    "phones": r"\b(?:\+?\d{1,3}[\s-]?)?\d{10}\b",
    "percentages": r"\b\d+(?:\.\d+)?%",
}

def extract(text: str) -> dict:
    out = {}
    for name, pat in PATTERNS.items():
        found = sorted(set(re.findall(pat, text)))
        if found:
            out[name] = found
    return out