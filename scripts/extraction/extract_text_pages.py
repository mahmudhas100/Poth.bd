import pdfplumber

def extract():
    with pdfplumber.open('raw_data/farecharts/brta-part3.pdf') as pdf:
        for i in range(28, 33):
            print(f"--- Page {i+1} ---")
            page = pdf.pages[i]
            print(page.extract_text())

if __name__ == "__main__":
    extract()
