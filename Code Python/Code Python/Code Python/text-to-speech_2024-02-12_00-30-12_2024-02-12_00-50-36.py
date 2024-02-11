import pyttsx3
import pdfplumber
from tqdm import tqdm
from pydub import AudioSegment
import os


pdfFile = input('Enter the file you want to convert (including .pdf extension): ')
audio_file = input("Enter the desired name for the output audio file (including .mp3 extension): ")
audio_format = input("Enter the audio format (mp3, wav, etc.): ")
audio_bitrate = input("Enter the desired bitrate (e.g., 192k, 256k): ")


#Initialize text-to-speech engine
engine = pyttsx3.init()

#listing available voices and allowing the user to choose his preferance
voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    print(f"{index}: Voice Id: {voice.id}, Language: {voice.languages}, Gender: {voice.gender}")

voice_number = int(input('Select the number of your preferred voice: '))
selected_voice_id = voices[voice_number].id

#set the chosen voice
engine.setProperty('voice', selected_voice_id)
#Set the speed of the speech
engine.setProperty('rate', 150)  


    


#saving the audiobook in a specific file & handeling errors
def process_text_to_audio(text, audio_file, format='mp3', bitrate='192K'):
    temp_audio = 'temp_audio.wav'
    
    try:
        engine.save_to_file(text, audio_file)
        engine.runAndWait()
        
        #convert to desired format using pydub
        audio = AudioSegment.from_wav(temp_audio)
        audio.export(audio_file, format=format, bitrate=bitrate)
    except Exception as e:
        print(f"An error occurred in text-to-speech conversion: {e}")
    finally:
        os.remove(temp_audio)
        
        
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
                
            
        process_text_to_audio(full_text, audio_file, format=audio_format, bitrate=audio_bitrate)
        
        print('Finished Processing Your File...ENJOY!')

except FileNotFoundError:
    print(f"The file {pdfFile} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")