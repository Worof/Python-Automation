import os
import shutil
import datetime
from tqdm import tqdm
import logging
import argparse

#adding command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description = 'File Organization Script')
    parser.add_argument('--images', nargs='+', help='Extensions for image files', default=[".png", ".jpg", ".jpeg", ".gif", ".tif", ".bmp"])
    parser.add_argument('--videos', nargs='+', help='Extensions for video files', default=[".mp4", ".mov", ".wmv", ".flv", ".mkv", ".avi"])
    parser.add_argument('--docs', nargs='+', help='Extensions for video files', default=[".pdf", ".doc", ".docx", ".html", ".htm", ".odt", ".xls", ".xlsx", ".ods", ".ppt", ".pptx", ".txt"])
    parser.add_argument('--archive', nargs='+', help='Extensions for image files', default=[".zip", ".rar"])
    parser.add_argument('--py', nargs='+', help='Extensions for video files', default=[".py"])
    parser.add_argument('--c', nargs='+', help='Extensions for video files', default=[".c"])
    parser.add_argument('--music', nargs='+', help='Extensions for video files', default=[".mp3", ".wav", ".flac", ".ogg"])
    parser.add_argument('--csv', nargs='+', help='Extensions for video files', default=[".csv", ".xlsb"])
    parser.add_argument('--undo', action='store_true', help='Undo the last organization operation') 
    return vars(parser.parse_args())

args = parse_arguments()

#configure your logging
logging.basicConfig(filename='file_organizer.log', level= logging.INFO,
                     format='%(asctime)s %(levelname)s: %(message)s')

#adding a dry run option for functionality
def get_dry_run_choice():
    choice = input("Do you want to perform a dry run first? (yes/no): ").lower()
    return choice == "yes"

dry_run = get_dry_run_choice()

#adding an undo functionality feature
def undo_last_operation(logfile='file_organizer.log'):
    move_operations = []
    with open(logfile, 'r') as f:
        # Reverse read the lines to get the move operations in reverse order
        for line in reversed(f.readlines()):
            if "INFO: Moved from" in line:
                # Extract the source and destination paths
                try:
                    parts = line.strip().split("'")
                    src = parts[1]  # The source path is the second element in the list
                    dst = parts[3]  # The destination path is the fourth element
                    move_operations.append((dst, src))  # Append as (destination, source) to reverse the move
                except IndexError:
                    # Skip lines that don't fit the expected format
                    continue

    # Perform the undo operations
    for src, dst in move_operations:
        try:
            if not os.path.exists(os.path.dirname(dst)):
                os.makedirs(os.path.dirname(dst))
            shutil.move(src, dst)
            print(f"Successfully reverted '{src}' to '{dst}'")
            logging.info(f"UNDO|{src}|{dst}")
        except Exception as e:
            print(f"Failed to revert '{src}' to '{dst}': {e}")
            logging.error(f"UNDO FAILED|{src}|{dst}")








                


current_dir = os.path.dirname(os.path.realpath(__file__))


file_ext_mapping = {
        # Images mapping
        'Images': args['images'],
        # Videos mapping
        'Videos': args['videos'],
        # Docs Mapping
        'Documents': args['docs'],
        # Archive Mapping
        'Archive': args['archive'],
        # Python code mapping
        "Code Python": args['py'],
        # C code mapping
        "Code C": args['c'],
        # Music mapping
        "Music": args['music'],
        # Spreadsheets mapping
        "Spreadsheets": args['csv']
    }

def rename_with_date(filename):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        basename, extension = os.path.splitext(filename)
        return f"{basename}_{timestamp}{extension}"
    
if args['undo']:
    undo_last_operation()
else:
    for filename in tqdm(os.listdir(current_dir), desc='Organized Files Are in Progress', unit="file"):
     file_extension = os.path.splitext(filename)[1].lower()
     for  folder_name, extensions in file_ext_mapping.items():
             if file_extension in [ext.lower() for ext in extensions]:
                destination_folder = os.path.join(current_dir, folder_name)
                if not os.path.exists(destination_folder):
                     os.makedirs(destination_folder)
                logging.info(f"Created directory: {destination_folder}")
                new_filename = rename_with_date(filename)
                src_path = os.path.join(current_dir, filename)
                dst_path = os.path.join(destination_folder, new_filename)
                if dry_run:
                 print(f"[DRY RUN] Would move '{src_path}' to '{dst_path}'")
                
                try:
                 shutil.move(src_path, dst_path)
                 logging.info(f"Moved from '{src_path}' to '{dst_path}'")
                except Exception as e:
                    logging.error(f"Failed to move '{src_path}' to '{dst_path}'")




