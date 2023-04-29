import os
import xylozi_common as com
import re
import random

province_dir = "C:\\Users\\Xylozi\\Documents\\Paradox Interactive\\Europa Universalis IV\\mod\\fallout_wild_wasteland\\history\\provinces\\"

template = com.get_file_as_string("capitals.txt")
capitals = template.split(" ")

os.chdir(province_dir)

for (dirpath, dirnames, filenames) in os.walk(province_dir):
    for filename in filenames:
        id = filename.split(" - ")[0]
        file_contents = com.get_file_as_string(filename)

        # Base Tax
        rand_min = 1
        rand_max = 3

        # Is capital
        if id in capitals:
            rand_min = 3
            rand_max = 8

        file = open(filename, "wt")
        file_contents = re.sub("base_tax = .*", "base_tax = {0}".format(random.randrange(rand_min, rand_max)), file_contents)
        file_contents = re.sub("base_production = .*", "base_production = {0}".format(random.randrange(rand_min, rand_max)), file_contents)
        file_contents = re.sub("base_manpower = .*", "base_manpower = {0}".format(random.randrange(rand_min, rand_max)), file_contents)
        file.write(file_contents)
        file.close()

