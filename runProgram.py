import os
from pathlib import Path
from colorama import init
from subprocess import run
from colorama import Fore  # Color in windows and linux
import sys

from renameFile import renameFile
from function_getMetadata import getAndSaveMetadata
from main2 import main2

def runProgram(filename, outputFileName, filenameAndDirectory, iterations, failedFiles, warningFiles, outputFileNameAndDirectory, currentOS):

    # Check If File Exists

    if os.path.isfile(outputFileNameAndDirectory):
        print(Fore.MAGENTA + "All ready exists: " + outputFileName + Fore.RESET)
        return  # Skip this loop were done here

    print(Fore.BLUE + "Started: " + filename + Fore.RESET, end='\r')  # Print and return courser to the start of the line

    iterations += 1  # Log how many files we change

    try:  # Skip loop if theres a problem with the file
        metadataTable, totalNumOfStreams = getAndSaveMetadata(filename, filenameAndDirectory)  # Get metadata
    except:
        failedFiles += 1  # Add to failed count
        iterations -= 1  # Remove from successful count
        return

    # Process metadata
    metadataAndMaps = main2(filenameAndDirectory, metadataTable, totalNumOfStreams, currentOS)

    if currentOS == "Linux":
        print("ffmpeg -v error -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0 "+metadataAndMaps+" -metadata title=\"\" -c copy -copy_unknown \"" + outputFileNameAndDirectory + "\"")
        errorCheck = run("ffmpeg -v error -xerror -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" + metadataAndMaps + " -metadata title=\"\" -c copy -copy_unknown \"" + outputFileNameAndDirectory + "\"", capture_output=True, shell=True)

    elif currentOS == "Windows":
        # Output:
        # print("ffmpeg -v error -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0 "+metadataAndMaps+" -metadata title=\"\" -c copy -copy_unknown \"" + outputFileNameAndDirectory + "\"")
        errorCheck = run("cmd /c ffmpeg -v error -xerror -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" + metadataAndMaps + " -metadata title=\"\" -c copy -copy_unknown \"" + outputFileNameAndDirectory + "\"", capture_output=True, shell=True)

    if str(errorCheck.stderr) != "b\'\'":  # Integrity and error check
        print(str(errorCheck.stderr))
        length = len(Fore.BLUE + "Started: " + filename + Fore.RESET)
        negLength = len(Fore.YELLOW + "May Be Corrupted: " + filename + Fore.RESET)
        littleSpaces = ' ' * (length - negLength)  # Pack the output with spaces or there will be characters left from the overwritten print

        print(Fore.YELLOW + "May Be Corrupted: " + filename + Fore.RESET + littleSpaces)
        warningFiles += 1
        iterations -= 1  # Remove from successful count
        os.remove(Path(outputFileNameAndDirectory))  # Delete the file since its corrupted
        return

    length = len(Fore.BLUE + "Starting: " + filename + Fore.RESET)
    negLength = len(Fore.GREEN + "Done: " + outputFileName + Fore.RESET)
    spaces = ' ' * (length - negLength)  # Pack the output with spaces or there will be characters left from the overwritten print

    print(Fore.GREEN + "Done: " + outputFileName + Fore.RESET + spaces)
    return iterations, failedFiles, warningFiles
