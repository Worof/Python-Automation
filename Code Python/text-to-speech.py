import pyttsx3
import pdfplumber
from tqdm import tqdm

pdfFile = 'great-expectations.pdf'


#Initialize text-to-speech engine
engine = pyttsx3.init()
#Set the speed of the speech
engine.setProperty('rate', 150)  


#saving the audiobook in a specific file & handeling errors
def process_text_to_audio(text, file_name):
    try:
        engine.save_to_file(text, file_name)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred in text-to-speech conversion: {e}")
#converting the book into audiobook in chunks 
try:
    with pdfplumber.open(pdfFile) as pdf:
        total_pages = len(pdf.pages)
        print(f"Processing {total_pages} pages...")

        for i, page in enumerate(tqdm(pdf.pages, desc='Converting Pages into Audio')):
            text = page.extract_text()
            if text:
                audio_file = f'great-expectations_page_{i+1}.mp3'
                process_text_to_audio(text, audio_file)
        print('Finished Processing Your File...ENJOY!')

except FileNotFoundError:
    print(f"The file {pdfFile} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")