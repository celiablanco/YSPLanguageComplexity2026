import pdfplumber

with pdfplumber.open("hebrew.pdf") as pdf, open("hebrew.txt", "w", encoding="ASC") as f:
    
    for page in pdf.pages:
        t = page.extract_text()
        if t:
            f.write(t + '\n')