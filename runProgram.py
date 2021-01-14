import os
from pathlib import Path
from subprocess import run
import subprocess
from colorama import Fore  # Color in windows and linux
import re

from function_getMetadata import getAndSaveMetadata
from function_addMetadataAndMaps import addMetadataAndMaps

def runProgram(filename, outputFileName, filenameAndDirectory, iterations, failedFiles, warningFiles, outputFileNameAndDirectory, currentOS, engAudioNoSubs):

    # Check If File Exists

    if os.path.isfile(outputFileNameAndDirectory):
        print(Fore.MAGENTA + "All ready exists: " + outputFileName + Fore.RESET)
        return iterations, failedFiles, warningFiles  # Skip this loop were done here


    print(Fore.BLUE + "Started: " + filename + Fore.RESET, end="\r")  # Print and return courser to the start of the line
    #print(Fore.BLUE + "Started: " + filename + Fore.RESET)  # Debugging

    iterations += 1  # Log how many files we change

    try:  # Skip loop if theres a problem with the file
        metadataTable, totalNumOfStreams = getAndSaveMetadata(filename, filenameAndDirectory)  # Get metadata
    except:
        failedFiles += 1  # Add to failed count
        iterations -= 1  # Remove from successful count
        return iterations, failedFiles, warningFiles

    # Process metadata
    metadataAndMaps, foreignWarning = addMetadataAndMaps(filenameAndDirectory, metadataTable, totalNumOfStreams, currentOS, engAudioNoSubs)
    if foreignWarning is True:
        print(Fore.Yellow + "There was no English Subtitles to go with Foreign Audio: " + outputFileName + Fore.RESET)
        warningFiles += 1
        iterations -= 1
        return iterations, failedFiles, warningFiles  # Skip this loop were done here

    if currentOS == "Linux":
        #print("ffmpeg -v error -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0 "+metadataAndMaps+" -metadata title=\"\" -c copy -copy_unknown \"" + outputFileNameAndDirectory + "\"")
        errorCheck = run("ffmpeg -v error -xerror -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" + metadataAndMaps + " -metadata title=\"\" -c copy -copy_unknown \"" + outputFileNameAndDirectory + "\"", capture_output=True, shell=True)

    elif currentOS == "Windows":
        # Output:
        print("ffmpeg -v error -xerror -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" + metadataAndMaps + " -metadata title=\"\" -c copy -copy_unknown \"" + outputFileNameAndDirectory + "\"")
        errorCheck = run("cmd /c ffmpeg -v error -xerror -n -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" + metadataAndMaps + " -metadata title=\"\" -c copy -copy_unknown \"" + outputFileNameAndDirectory + "\"", capture_output=True, shell=True)

        if len(str(errorCheck.stderr)) > 8:  # Integrity and error check
            if str(errorCheck.stderr).find("Referenced QT chapter track not found") != -1:
                print(filename + Fore.YELLOW + " Was a non standard file" + Fore.RESET)
            else:
                errorOutput = re.sub("b\'", "", str(errorCheck.stderr))
                errorOutput = re.sub(r"\\r\\n\'", "", errorOutput)
                print(Fore.YELLOW + "FFmpeg Error: " + "\"" + Fore.RESET + errorOutput + Fore.YELLOW + "\"" + Fore.RESET)

                packingSpaces = ' ' * (len(Fore.BLUE + "Started: " + filename + Fore.RESET) - len(Fore.YELLOW + "May Be Corrupted: " + filename + Fore.RESET))  # Pack the output with spaces or there will be characters left from the overwritten print
                print(Fore.YELLOW + "May Be Corrupted: " + filename + Fore.RESET + packingSpaces)
                warningFiles += 1
                iterations -= 1  # Remove from successful count
                try:
                    os.remove(Path(outputFileNameAndDirectory))  # Delete the file since its corrupted
                except:
                    print(":o Could not delete " + outputFileNameAndDirectory)
                return iterations, failedFiles, warningFiles

    packingSpaces = " " * (len(Fore.BLUE + "Started: " + filename + Fore.RESET) - len(Fore.GREEN + "Done: " + outputFileName + Fore.RESET))  # Pack the output with spaces or there will be characters left from the overwritten print
    print(Fore.GREEN + "Done: " + outputFileName + Fore.RESET + packingSpaces)
    return iterations, failedFiles, warningFiles
