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

from renameFile import renameFile
from function_getMetadata import getAndSaveMetadata
from main2 import main2

init()  # Stops makes sure windows displays colour

directory = os.path.dirname(os.path.realpath(__file__))

print(Fore.YELLOW + "W" + Fore.WHITE + "e" + Fore.GREEN + "l" + Fore.BLUE + "c" + Fore.MAGENTA + "o" + Fore.RED + "m" + Fore.CYAN + "e" + Fore.RESET + " to Standard Format Transcoder")

input("Press Enter to start...")

#print(platform.system())

#print(directory)
#print(os.listdir(directory))

print("Transcode Starting")
Path("MKVoutput/").mkdir(parents=True, exist_ok=True)
#Path("Metadata/").mkdir(parents=True, exist_ok=True)

iterations = 0
failedFiles = 0
warningFiles = 0
for filename in os.listdir(directory):
    if filename.endswith(".mkv"):  # Find Any MKV files

        outputfilename = renameFile(filename)  # Rename File

        # Check If File Exists
        if os.path.isfile("MKVoutput/"+outputfilename):
            print(Fore.MAGENTA + "All ready exists: "+outputfilename + Style.RESET_ALL)
            continue  # Skip this loop were done here
        print(Fore.BLUE + "Started: " + filename + Style.RESET_ALL, end='\r')  # Print and return courser to the start of the line

        iterations += 1  # Log how many files we change
        streamNum = 0

        try:  # Skip loop if theres a problem wit the file
            metadataTable, totalNumOfStreams = getAndSaveMetadata(filename)
        except:
            failedFiles += 1  # Add to failed count
            iterations -= 1  # Remove from successful count
            continue


        # Open Metadata file for processing

        metadataAndMaps = main2(filename, metadataTable, totalNumOfStreams)

        #print("")

        #print("ffmpeg -v error -n -i \""+filename+"\" -map_metadata -1 -map_chapters 0 "+metadataAndMaps+" -metadata title=\"\" -c copy -copy_unknown \"MKVoutput\\"+outputfilename+"\"")

        errorCheck = run("cmd /c ffmpeg -v error -xerror -n -i \""+filename+"\" -map_metadata -1 -map_chapters 0"+metadataAndMaps+" -metadata title=\"\" -c copy -copy_unknown \"MKVoutput\\"+outputfilename+"\"", capture_output=True, shell=True)

        if str(errorCheck.stderr) != "b\'\'":  # Integrity check
            print(Fore.YELLOW + "May Be Corrupted: " + filename + Fore.RESET)
            warningFiles += 1
            iterations -= 1  # Remove from successful count
            os.remove("MKVoutput/" + outputfilename)  # Delete the file since its corrupted
            continue


        length = len(Fore.BLUE + "Starting: " + filename + Style.RESET_ALL)
        negLength = len(Fore.GREEN + "Done: " + outputfilename + Style.RESET_ALL)
        spaces = ' ' * (length - negLength)  # Pack the output with spaces or there will be characters left from the overwritten print

        print(Fore.GREEN + "Done: " + outputfilename + Style.RESET_ALL + spaces)

if iterations != 0:
    print("Finished", iterations, "files")
if failedFiles != 0:
    print(Fore.RED + str(failedFiles) + " Failed" + Fore.RESET)
if warningFiles != 0:
    print(Fore.YELLOW + str(warningFiles) + " Warnings" + Fore.RESET)
input("Press ENTER to exit...")

