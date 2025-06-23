import fitz
import pandas as pd

def parse_pdf(path: str) -> str:
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

# Add Excel or JSON parsers as needed