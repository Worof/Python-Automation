import os
import shutil
import datetime
#from tqdm import tqdm
import logging
import argparse
#import errno
import json 

#adding command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description = 'File Organization Script')
    parser.add_argument('--config', type=str, help='Path to the configuration file', default='config.json')
    parser.add_argument('--undo', action='store_true', help='Undo the last organization operation') 
    return vars(parser.parse_args())

args = parse_arguments()

#configure your logging
logging.basicConfig(filename='file_organizer.log', level= logging.INFO,
                     format='%(asctime)s %(levelname)s: %(message)s')
#load configuration from the json file
def load_configuration(config_path):
    if not os.path.exists(config_path):
        logging.error(f"Configuration file not found at {config_path}")
        print(f"Configuration file not found at {config_path}. Using default settings.")
        return None
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from the configuration file: {e}")
        print(f"Error decoding JSON from the configuration file. Please check the file format.")
        return None

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
            
# Define sensitive criteria
sensitive_extensions = ['.key', '.pem', '.env']

def is_sensitive_file(filename):
    if any(filename.endswith(ext) for ext in sensitive_extensions):
        return True
    return False

def handle_sensitive_file(filename, src_path):
    print(f"\nSensitive file detected: {filename}")
    print("This file is flagged as sensitive due to its type, name, or location.")
    action = input("Choose an action - (V)iew, (R)ename, (S)kip: ").lower()
    
    if action == 'v':
        # Adjust based on your file types
        with open(src_path, 'r') as f:
            print(f.read())
        return handle_sensitive_file(filename, src_path)
    
    elif action == 'r':
        new_name = input("Enter new name for the file: ")
        return os.path.join(os.path.dirname(src_path), new_name)
    
    elif action == 's':
        print(f"Skipping {filename}.\n")
        return None
    
    else:
        print("Invalid option selected.")
        return handle_sensitive_file(filename, src_path)
    
    
#check the disk space 
def check_disk_space(file_path, destination_dir):
    total, used, free = shutil.disk_usage(destination_dir)
    file_size = os.path.getsize(file_path)
    return file_size <= free








                


current_dir = os.path.dirname(os.path.realpath(__file__))


file_ext_mapping = load_configuration(args['config']) or {
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

"""def rename_with_date(filename):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        basename, extension = os.path.splitext(filename)
        return f"{basename}_{timestamp}{extension}" """
    
interactive_mode_enabled = input("Enable interactive mode? (yes/no): ").lower() == "yes"
    
if args['undo']:
    undo_last_operation()
else:
    for filename in os.listdir(current_dir):
        file_extension = os.path.splitext(filename)[1].lower()
        src_path = os.path.join(current_dir, filename)
        for folder_name, extensions in file_ext_mapping.items():
            if file_extension in [ext.lower() for ext in extensions]:
                destination_folder = os.path.join(current_dir, folder_name)
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                dst_path = os.path.join(destination_folder, filename)

                if os.path.exists(dst_path) and interactive_mode_enabled:
                    #handle filename conflict
                    action = input(f"File '{dst_path}' already exists. Do you want to (o)verwrite or (s)kip? [o/s]: ").lower()
                    if action == 's':
                        print(f"Skipping '{filename}'.")
                        continue
                    elif action == 'o' and not input(f"Are you sure you want to overwrite '{dst_path}'? [y/n]: ").lower() == 'y':
                        print(f"Skipping '{filename}'.")
                        continue

                if dry_run:
                    print(f"[DRY RUN] Would move '{filename}' to '{dst_path}'")
                    continue

                if not check_disk_space(src_path, destination_folder):
                    print(f"Not enough disk space to move '{filename}' to '{destination_folder}'.")
                    logging.error(f"Disk space error: Not enough space for '{filename}' in '{destination_folder}'.")
                    continue

                try:
                    shutil.move(src_path, dst_path)
                    logging.info(f"Moved from '{src_path}' to '{dst_path}'")
                except PermissionError:
                    print(f"Permission denied: Unable to move '{filename}' to '{dst_path}'.")
                    logging.error(f"PermissionError: Failed to move '{filename}' to '{dst_path}'.")
                except Exception as e:
                    print(f"Unexpected error moving '{filename}' to '{dst_path}': {e}")
                    logging.error(f"Unexpected error: {filename} to {dst_path}: {e}")

print("File organization complete.")
