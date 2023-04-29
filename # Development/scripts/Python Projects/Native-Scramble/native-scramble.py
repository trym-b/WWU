import os
import xylozi_common as com
import re
import random

template = com.get_file_as_string("list.txt")
provinces = template.split(" ")

list_1 = []
list_2 = []
list_3 = []
list_4 = []
list_5 = []
list_6 = []
list_7 = []
list_8 = []
list_9 = []
list_10 = []

for i in provinces:
    roll = random.randrange(1, 10)

    if roll == 1: list_1.append(i)
    elif roll == 2: list_2.append(i)
    elif roll == 3: list_3.append(i)
    elif roll == 4: list_4.append(i)
    elif roll == 5: list_5.append(i)
    elif roll == 6: list_6.append(i)
    elif roll == 7: list_7.append(i)
    elif roll == 8: list_8.append(i)
    elif roll == 9: list_9.append(i)
    elif roll == 10: list_10.append(i)

print( "###############" )
print( "List 1" )
print("###############")
line = ""
for i in list_1:
    line = line + i + " "
print(line)

print( "###############" )
print("List 2")
print("###############")
line = ""
for i in list_2:
    line = line + i + " "
print(line)

print("###############")
print("List 3")
print("###############")
line = ""
for i in list_3:
    line = line + i + " "
print(line)

print("###############")
print("List 4")
print("###############")
line = ""
for i in list_4:
    line = line + i + " "
print(line)

print("###############")
print("List 5")
print("###############")
line = ""
for i in list_5:
    line = line + i + " "
print(line)

print("###############")
print("List 6")
print("###############")
line = ""
for i in list_6:
    line = line + i + " "
print(line)

print("###############")
print("List 7")
print("###############")
line = ""
for i in list_7:
    line = line + i + " "
print(line)

print("###############")
print("List 8")
print("###############")
line = ""
for i in list_8:
    line = line + i + " "
print(line)

print("###############")
print("List 9")
print("###############")
line = ""
for i in list_9:
    line = line + i + " "
print(line)

