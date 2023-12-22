import pyttsx3
import pdfplumber
from tqdm import tqdm


pdfFile = 'great-expectations.pdf'

#Extract the text from the PDF file
finalText = []

try:
    with pdfplumber.open(pdfFile) as pdf:
        pages = len(pdf.pages)
        for page in tqdm(pdf.pages, desc ='Converting Pages into Audio'):
            text = page.extract_text()
            if text:
                finalText.append(text)
except FileNotFoundError:
    print(f"The file {pdfFile} was not found.")
    exit()
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

# Join all extracted text
finalText = '\n'.join(finalText)

        
#Convert the text into audio & save it
engine = pyttsx3.init()
engine.save_to_file(finalText, 'great-expectations.mp3')
engine.runAndWait()