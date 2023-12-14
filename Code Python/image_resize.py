import os
from PIL import Image

image_fit_size = int(input("Enter the Image Size: "))
output_folder = input("Enter the Directory of the Output Folder: ")

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Loop through all files in the current directory
for filename in os.listdir('.'):
    # Check if the file is an image
    if filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".tif")):
        # Open the Image
        image = Image.open(filename)

        # Get the Image Size
        width, height = image.size

        # Check if the image needs resizing
        if width > image_fit_size or height > image_fit_size:
            # Calculate new dimensions
            if width > height: 
                height = int((image_fit_size / width) * height)
                width = image_fit_size
            else:
                width = int((image_fit_size / height) * width)
                height = image_fit_size

            # Resizing the image
        image = image.resize((width, height))
        print('resizing : %s' %(filename))

        # Save the Image in the Output Folder Directory
        image.save(os.path.join(output_folder, filename))

print("----------------------------------------------")
print("Done Resizing All Images.")