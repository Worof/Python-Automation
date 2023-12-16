import os
import shutil
import logging  
import datetime  


current_dir = os.path.dirname(os.path.realpath(__file__))

##File Renaming##

# Rename files based on date:
def rename_with_date(filename):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    basename, extension = os.path.splitext(filename)
    return f"{basename}_{timestamp}{extension}"

#Organize images into image folder

for filename in os.listdir(current_dir):
      if filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".tif", ".bmp")):
        if not os.path.exists("Images"):
            os.mkdir('Images')
        new_filename = rename_with_date(filename)
        shutil.move(filename, os.path.join("Images", new_filename))
        
        
#organize video files into video folder
for filename in os.listdir(current_dir):
      if filename.endswith((".mp4", ".mov", ".wmv", ".flv", ".mkv", ".avi")):
        if not os.path.exists("Videos"):
            os.mkdir('Videos')
        new_filename = rename_with_date(filename)
        shutil.move(filename, os.path.join("Videos", new_filename))
        
#organize docs files into docs folder
for filename in os.listdir(current_dir):
      if filename.endswith((".pdf", ".doc", ".docx", ".html", ".htm", ".odt", ".xls", ".xlsx", ".ods", ".ppt", ".pptx", ".txt")):
        if not os.path.exists("Documents"):
            os.mkdir('Documents')
        new_filename = rename_with_date(filename)
        shutil.move(filename, os.path.join("Documents", new_filename))


#organize archives files into archive folder
for filename in os.listdir(current_dir):
      if filename.endswith((".zip", ".rar")):
        if not os.path.exists("Archive"):
            os.mkdir('Archive')
        new_filename = rename_with_date(filename)
        shutil.move(filename, os.path.join("Archive", new_filename))
        
#organize python codes' files into code folder
for filename in os.listdir(current_dir):
      if filename.endswith((".py")):
        if not os.path.exists("Code Python"):
            os.mkdir('Code Python')
        new_filename = rename_with_date(filename)
        shutil.move(filename, os.path.join("Code Python", new_filename))


#organize C codes' files into code folder
for filename in os.listdir(current_dir):
      if filename.endswith((".c")):
        if not os.path.exists("Code C"):
            os.mkdir('Code C')
        new_filename = rename_with_date(filename)
        shutil.move(filename, os.path.join("Code C", new_filename))
        
        
#organize music files into music folder
for filename in os.listdir(current_dir):
      if filename.endswith((".mp3", ".wav", ".flac", ".ogg")):
        if not os.path.exists("Music"):
            os.mkdir('Music')
        new_filename = rename_with_date(filename)
        shutil.move(filename, os.path.join("Music", new_filename))
        
#organize spreadsheets into music folder
for filename in os.listdir(current_dir):
      if filename.endswith((".csv", ".xlsb")):
        if not os.path.exists("Spreadsheets"):
            os.mkdir('Spreadsheets')
        new_filename = rename_with_date(filename)
        shutil.move(filename, os.path.join("Spreadsheets", new_filename))      


