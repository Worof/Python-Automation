import os
import shutil
import datetime
from tqdm import tqdm



current_dir = os.path.dirname(os.path.realpath(__file__))


file_ext_mapping = {
        # Images mapping
        (".png", ".jpg", ".jpeg", ".gif", ".tif", ".bmp"): 'Images',
        # Videos mapping
        (".mp4", ".mov", ".wmv", ".flv", ".mkv", ".avi"): 'Videos',
        # Docs Mapping
        (".pdf", ".doc", ".docx", ".html", ".htm", ".odt", ".xls", ".xlsx", ".ods", ".ppt", ".pptx", ".txt"): 'Documents',
        # Archive Mapping
        (".zip", ".rar"): 'Archive',
        # Python code mapping
        (".py",): "Code Python",
        # C code mapping
        (".c",): "Code C",
        # Music mapping
        (".mp3", ".wav", ".flac", ".ogg"): "Music",
        # Spreadsheets mapping
        (".csv", ".xlsb"): "Spreadsheets"
    }

def rename_with_date(filename):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        basename, extension = os.path.splitext(filename)
        return f"{basename}_{timestamp}{extension}"

for filename in tqdm(os.listdir(current_dir), desc='Organized Files Are in Progress', unit="file"):
        for extensions, folder_name in file_ext_mapping.items():
            if filename.endswith(extensions):
                destination_folder = os.path.join(current_dir, folder_name)
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                new_filename = rename_with_date(filename)
                src_path = os.path.join(current_dir, filename)
                dst_path = os.path.join(destination_folder, new_filename)
                shutil.move(src_path, dst_path)



