import pyttsx3
import pdfplumber
from tqdm import tqdm

pdfFile = '1984.pdf'
audio_file = '1984-audiobook.mp3'


#Initialize text-to-speech engine
engine = pyttsx3.init()
#Set the speed of the speech
engine.setProperty('rate', 120)  


#saving the audiobook in a specific file & handeling errors
def process_text_to_audio(text):
    try:
        engine.save_to_file(text, audio_file)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred in text-to-speech conversion: {e}")
        
        
#converting the book into audiobook in chunks 


try:
    with pdfplumber.open(pdfFile) as pdf:
        total_pages = len(pdf.pages)
        print(f"Processing {total_pages} pages...")
        full_text = ''

        for i, page in enumerate(tqdm(pdf.pages, desc='Converting Pages into Audio')):
            text = page.extract_text()
            if text:
                full_text += text + ''
                
            
        process_text_to_audio(full_text)
        
        print('Finished Processing Your File...ENJOY!')

except FileNotFoundError:
    print(f"The file {pdfFile} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")