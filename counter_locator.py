import csv, re, os

# Variables for the directory

while True:
  try:
    dir = os.getcwd()
    filebulk = "bulkstatsschema.csv"
    print()
    filename = input("Please type the name of the file?(default: bulkstatsschema.csv) ")
    if filename == "" or filename == filebulk:
      filepath = f"{dir}\\{filebulk}"
    else:
      filepath = f"{dir}\\{filename}"

    csvfile = open(f"{filepath}")
    break
  except FileNotFoundError:
    print("File does not exist in this folder. Please fix the filename or folder.")
    continue

# Function to check the format of the counter
def validate_counter(counter):
  regex = re.compile(r"^%?([\w\-?])+%?$")
  if regex.match(counter):
    return True
  else:
    return False

# Applying the counter

while True:
  csvfile = open(f"{filepath}")
  file = csv.reader(csvfile)
  counter = input("\nPlease type the counter. Formats(%xxx-xxx-xxx...%, xxx-xxx-xxx): ")
  validation = validate_counter(counter)
  if validation:
    print()
    counter_re = re.compile(r"^%([\w\-?])+%$")
    if (counter_re.match(counter)):
      # Searching for the position and schema for the counter.
      for row_num in file:
        rowsize = len(row_num)
        for i in range(rowsize-1):
          if (bool(row_num) == True):
            if (row_num[i] == counter):
              print("="*79)
              print(f"Counter: {row_num[i]} \nSchema: {row_num[2]} \nposition: {row_num[2:].index(row_num[i])}")
              print("="*79)
              break
    else:
      counter = f"%{counter}%"
      for row_num in file:
        rowsize = len(row_num)
        for i in range(rowsize-1):
          if (bool(row_num) == True):
            if (row_num[i] == counter):
              print("="*79)
              print(f"Counter: {row_num[i]} \nSchema: {row_num[2]} \nposition: {row_num[2:].index(row_num[i])}")
              print("="*79)
              break
  else:
    print("*** ERROR! Wrong counter format, please type again. ***")
    continue

  answer = input("\nWould you like to search another counter? (Yes/No) ")
  pattern_yes = re.compile(r"[yY][eE]?[Ss]?")
  pattern_no = re.compile(r"[nN][oO]?")

  if pattern_yes.match(answer):
      continue
  elif pattern_no.match(answer):
      print("\nThank you!!! \n")
      break
  else:
      print("\nYou typed something different from yes and no. Closing the program...\n")
      break