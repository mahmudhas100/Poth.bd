import pypdfium2 as pdfium
import os
from PIL import Image

PDF_DIR = "raw_data/revised_farecharts"
IMG_DIR = "raw_data/revised_images"
os.makedirs(IMG_DIR, exist_ok=True)

def process_pdfs():
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, filename)
            pdf = pdfium.PdfDocument(pdf_path)
            n_pages = len(pdf)
            
            print(f"Processing {filename} ({n_pages} pages)...")
            
            for i in range(n_pages):
                page = pdf[i]
                bitmap = page.render(scale=300/72) # 300 DPI for high quality OCR
                pil_image = bitmap.to_pil()
                
                # Save as PNG
                img_name = f"{filename.replace('.pdf', '')}_page_{i+1}.png"
                pil_image.save(os.path.join(IMG_DIR, img_name))
                print(f"  ✓ Saved page {i+1}")

if __name__ == "__main__":
    process_pdfs()
