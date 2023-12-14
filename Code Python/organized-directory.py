import os
import shutil

current_dir = os.path.dirname(os.path.realpath(__file__))

#Organize iamges into image folder

for filename in os.listdir(current_dir):
      if filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".tif")):
        if not os.path.exists("Images"):
            os.mkdir('Images')
        shutil.copy(filename, 'Images')
        os.remove(filename)
        
        

        
#organize video files into video folder
for filename in os.listdir(current_dir):
      if filename.endswith((".mp4", ".mov", ".wmv", ".flv", ".mkv")):
        if not os.path.exists("Videos"):
            os.mkdir('Videos')
        shutil.copy(filename, 'Videos')
        os.remove(filename)
        
#organize docs files into docs folder
for filename in os.listdir(current_dir):
      if filename.endswith((".pdf", ".doc", ".docx", ".html", ".htm", ".odt", ".xls", ".xlsx", ".ods", ".ppt", ".pptx", ".txt")):
        if not os.path.exists("Documents"):
            os.mkdir('Documents')
        shutil.copy(filename, 'Documents')
        os.remove(filename)


#organize archives files into archive folder
for filename in os.listdir(current_dir):
      if filename.endswith((".zip", ".rar")):
        if not os.path.exists("Archive"):
            os.mkdir('Archive')
        shutil.copy(filename, 'Archive')
        os.remove(filename)
        
#organize codes' files into code folder
for filename in os.listdir(current_dir):
      if filename.endswith((".py")):
        if not os.path.exists("Code Python"):
            os.mkdir('Code Python')
        shutil.copy(filename, 'Code Python')
        os.remove(filename)