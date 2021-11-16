import csv, re, os, signal
from colorama import Fore, init, deinit, Back, Style

# Initialize Colorama for Windows
init()

signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl+C

# Variables for the directory
while True:
  check_filename = re.compile(r"^[cC]:.+\.csv$")
  try:
    dir = os.getcwd()
    filebulk = "bulkstatsschema.csv"
    print(Fore.CYAN, end="")
    print(Style.BRIGHT)
    filename = input(f"Please type the name or complete path of the file?(default: bulkstatsschema.csv) ")
    print(Style.RESET_ALL, end="")
    if filename == "" or filename == filebulk:
      filepath = f"{dir}\\{filebulk}"
    elif check_filename.match(filename):
      filepath = f"{filename}"
    else:
      filepath = f"{dir}\\{filename}"

    csvfile = open(f"{filepath}")
    break
  except FileNotFoundError:
    print()
    print(Fore.RED+"~"*79)
    print(f"File does not exist in the folder below. Please type the complete path.")
    print(f"{filepath}")
    print("~"*79+Fore.RESET)
    continue

# Function to check the format of the counter
def validate_counter(counter):
  regex = re.compile(r"^%?([\w\-?])+%?$")
  not_regex = re.compile(r"^%?(epochtime|localdate|localtime|uptime)%?$")
  if not_regex.match(counter):
    return False
  elif regex.match(counter):
    return True
  else:
    return False

# Applying the counter

while True:
  def run():
    csvfile = open(f"{filepath}")
    file = csv.reader(csvfile)
    print(Fore.CYAN, Style.BRIGHT, end="")
    print("\nPlease type the counter(s) with comma separated. Formats(%xxx-xxx-xxx...%,xxx-xxx-xxx):", Style.RESET_ALL, end = "")    
    counters = input()
    counters = counters.split(",")
    size_counters = len(counters)
    for counter in counters:
      csvfile = open(f"{filepath}")
      file = csv.reader(csvfile)
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
                  print(Style.BRIGHT)
                  print(f"{Fore.GREEN}="*79)
                  print(f"Counter: {row_num[i]} \nSchema: {row_num[2]} \nposition: {row_num[2:].index(row_num[i])}")
                  print("="*79 + f"{Style.RESET_ALL}")
                  if (size_counters == (counters.index(counter)+1)):
                    return

        else:
          percentage_counter = f"%{counter}%"
          # print(counters, counter, percentage_counter)
          for row_num in file:
            rowsize = len(row_num)
            for i in range(rowsize-1):
              if (bool(row_num) == True):
                if (row_num[i] == percentage_counter):
                  print(Style.BRIGHT)
                  print(f"{Fore.GREEN}="*79)
                  print(f"Counter: {row_num[i]} \nSchema: {row_num[2]} \nposition: {row_num[2:].index(row_num[i])}")
                  print("="*79 + f"{Style.RESET_ALL}")
                  if (size_counters == (counters.index(counter)+1)):
                    return

      else:
        print(Style.BRIGHT)
        print(f"{Fore.RED}*** ERROR! Wrong format or cannot be this counter. Please type again. ***{Style.RESET_ALL}")
        del counter
        run()
    else:
      try:
        print(f"{Style.BRIGHT}{Fore.RED}*** ERROR! Counter {counter} does not exist. Please retype the counters. ***{Style.RESET_ALL}")
        run()
      except UnboundLocalError:
        return
  
  run()
  
  print(f"{Fore.CYAN}{Style.BRIGHT}\nWould you like to search another counter? (Yes/No)", Style.RESET_ALL, end="")
  answer = input()
  pattern_yes = re.compile(r"^[yY][eE]?[Ss]?")
  pattern_no = re.compile(r"^[nN][oO]?")

  if pattern_yes.match(answer):
    continue
  elif pattern_no.match(answer):
    print("\nThank you!!! \n")
    deinit()
    break
  else:
    print("\nYou typed something different from yes and no. Closing the program...\n")
    deinit()
    break

deinit()