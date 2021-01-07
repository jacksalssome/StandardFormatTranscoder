import os
from pathlib import Path
import shutil
import subprocess
import re
import platform
from pathlib import Path
from colorama import init
from subprocess import run
from colorama import Fore, Back, Style  # Color in windows and linux
import sys
import argparse

from renameFile import renameFile
from function_getMetadata import getAndSaveMetadata
from main2 import main2


def runProgram(filename, outputFileName, filenameAndDirectory, iterations, failedFiles, warningFiles, outputFileNameAndDirectory):

    # Check If File Exists
    if os.path.isfile(outputFileNameAndDirectory):
        print(Fore.MAGENTA + "All ready exists: " + outputFileName + Style.RESET_ALL)
        return  # Skip this loop were done here
    print(Fore.BLUE + "Started: " + filename + Style.RESET_ALL, end='\r')  # Print and return courser to the start of the line

    iterations += 1  # Log how many files we change
    streamNum = 0

    try:  # Skip loop if theres a problem with the file
        metadataTable, totalNumOfStreams = getAndSaveMetadata(filename, filenameAndDirectory)
    except:
        failedFiles += 1  # Add to failed count
        iterations -= 1  # Remove from successful count
        return

    # Open Metadata file for processing

    metadataAndMaps = main2(filenameAndDirectory, metadataTable, totalNumOfStreams)

    # print("")

    #print("ffmpeg -v error -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0 "+metadataAndMaps+" -metadata title=\"\" -c copy -copy_unknown \"" + outputFileNameAndDirectory + "\"")

    errorCheck = run("cmd /c ffmpeg -v error -xerror -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" + metadataAndMaps + " -metadata title=\"\" -c copy -copy_unknown \"" + outputFileNameAndDirectory + "\"", capture_output=True, shell=True)

    if str(errorCheck.stderr) != "b\'\'":  # Integrity check

        length = len(Fore.BLUE + "Started: " + filename + Style.RESET_ALL)
        negLength = len(Fore.YELLOW + "May Be Corrupted: " + filename + Fore.RESET)
        littleSpaces = ' ' * (length - negLength)  # Pack the output with spaces or there will be characters left from the overwritten print

        print(Fore.YELLOW + "May Be Corrupted: " + filename + Fore.RESET + littleSpaces)
        warningFiles += 1
        iterations -= 1  # Remove from successful count
        os.remove(Path(outputFileNameAndDirectory))  # Delete the file since its corrupted
        return

    length = len(Fore.BLUE + "Starting: " + filename + Style.RESET_ALL)
    negLength = len(Fore.GREEN + "Done: " + outputFileName + Style.RESET_ALL)
    spaces = ' ' * (length - negLength)  # Pack the output with spaces or there will be characters left from the overwritten print

    print(Fore.GREEN + "Done: " + outputFileName + Style.RESET_ALL + spaces)
    return iterations, failedFiles, warningFiles
