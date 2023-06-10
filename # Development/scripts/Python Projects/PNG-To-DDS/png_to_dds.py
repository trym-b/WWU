from wand import image
import sys
import os

file_paths = sys.argv[1:]  # the first argument is the script itself
dropped_dir = file_paths[0]

os.chdir(dropped_dir)

for (dirpath, dirnames, filenames) in os.walk(dropped_dir):
    for filename in filenames:
        if ".png" in filename:
            new_filename = filename.replace("png", "dds")

            with image.Image(filename=filename) as img:
                img.compression = 'dxt5'
                img.save(filename=new_filename)

