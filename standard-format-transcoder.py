import os
from pathlib import Path
import shutil
import subprocess
import re
import platform
from pathlib import Path
from colorama import init
from subprocess import run
from colorama import Fore, Back, Style # Color in windows and linux
import sys
import argparse

from renameFile import renameFile
from function_getMetadata import getAndSaveMetadata
from main2 import main2

init()  # Stops makes sure windows displays colour

print(Fore.YELLOW + "W" + Fore.WHITE + "e" + Fore.GREEN + "l" + Fore.BLUE + "c" + Fore.MAGENTA + "o" + Fore.RED + "m" + Fore.CYAN + "e" + Fore.RESET + " to Standard Format Transcoder")

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="\"input filename\"")
args, unknown = parser.parse_known_args()

if unknown:
    print(Fore.YELLOW + "Don't know what this is: " + Fore.RESET + str(unknown))
    print(Fore.YELLOW + "Make sure there are quotes (\"\") around the directory if there are spaces in it." + Fore.RESET)
    input("Press Enter to exit...")
    sys.exit()

if not args.input: # If not user doesn't input a directory, make sure then run the program in current dir
    print(Fore.YELLOW + "No Directory was inputted, do you want to run in the current directory:" + Fore.RESET)
    print(str(os.path.dirname(os.path.realpath(__file__))) + Fore.YELLOW + "? [Y/N]" + Fore.RESET)
    answerYN = None
    while answerYN not in ("yes", "no", "y", "n"):
        answerYN = input()
        if answerYN == "yes" or answerYN == "y":
            directory = os.path.dirname(os.path.realpath(__file__))
        elif answerYN == "no" or answerYN == "n":
            sys.exit()
        else:
            print("Please enter yes or no.")
elif os.path.exists(args.input):
    directory = args.input
    if os.path.isfile(directory):
        print(Fore.YELLOW + "Cant handle direct files, only the directory they are in." + Fore.RESET)
        print(Fore.YELLOW + "Would you like to covert all files in this directory: " + Fore.RESET + "\"" + os.path.dirname(directory) + "\"" + Fore.YELLOW + "? [Y/N]" + Fore.RESET)
        answerYN = None
        while answerYN not in ("yes", "no", "y", "n"):
            answerYN = input()
            if answerYN == "yes" or answerYN == "y":
                directory = os.path.dirname(directory)
            elif answerYN == "no" or answerYN == "n":
                sys.exit()
            else:
                print("Please enter yes or no.")
else:
    print(Fore.YELLOW + "Can't find file path: " + args.input + Fore.RESET)
    input("Press Enter to exit...")
    sys.exit()

#print(platform.system())

#print(os.listdir(directory))

#print("Transcode Starting")
Path(directory + "\\" + "MKVoutput/").mkdir(parents=True, exist_ok=True)
#Path("Metadata/").mkdir(parents=True, exist_ok=True)

iterations = 0
failedFiles = 0
warningFiles = 0
for filename in os.listdir(directory):
    if filename.endswith(".mkv"):  # Find Any MKV files

        outputFileName = directory + "\\" + "MKVoutput\\" + renameFile(filename)  # Rename File and put it in MKVoutput directory
        filenameAndDirectory = directory + "\\" + filename  # Absoulte path to file

        # Check If File Exists
        if os.path.isfile(outputFileName):
            print(Fore.MAGENTA + "All ready exists: " + outputFileName + Style.RESET_ALL)
            continue  # Skip this loop were done here
        print(Fore.BLUE + "Started: " + filename + Style.RESET_ALL, end='\r')  # Print and return courser to the start of the line

        iterations += 1  # Log how many files we change
        streamNum = 0

        try:  # Skip loop if theres a problem wit the file
            metadataTable, totalNumOfStreams = getAndSaveMetadata(filename, filenameAndDirectory)
        except:
            failedFiles += 1  # Add to failed count
            iterations -= 1  # Remove from successful count
            continue


        # Open Metadata file for processing

        metadataAndMaps = main2(filenameAndDirectory, metadataTable, totalNumOfStreams)

        #print("")

        #print("ffmpeg -v error -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0 "+metadataAndMaps+" -metadata title=\"\" -c copy -copy_unknown \"" + outputFileName + "\"")

        errorCheck = run("cmd /c ffmpeg -v error -xerror -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" + metadataAndMaps + " -metadata title=\"\" -c copy -copy_unknown \"" + outputFileName + "\"", capture_output=True, shell=True)

        if str(errorCheck.stderr) != "b\'\'":  # Integrity check
            print(Fore.YELLOW + "May Be Corrupted: " + filename + Fore.RESET)
            warningFiles += 1
            iterations -= 1  # Remove from successful count
            os.remove(outputFileName)  # Delete the file since its corrupted
            continue


        length = len(Fore.BLUE + "Starting: " + filename + Style.RESET_ALL)
        negLength = len(Fore.GREEN + "Done: " + outputFileName + Style.RESET_ALL)
        spaces = ' ' * (length - negLength)  # Pack the output with spaces or there will be characters left from the overwritten print

        print(Fore.GREEN + "Done: " + outputFileName + Style.RESET_ALL + spaces)

if iterations != 0:
    print("Finished", iterations, "files")
if failedFiles != 0:
    print(Fore.RED + str(failedFiles) + " Failed" + Fore.RESET)
if warningFiles != 0:
    print(Fore.YELLOW + str(warningFiles) + " Warnings" + Fore.RESET)
input("Press ENTER to exit...")

