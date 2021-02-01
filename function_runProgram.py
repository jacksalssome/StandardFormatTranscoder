import os
from pathlib import Path
from subprocess import run
from colorama import Fore  # Color in windows and linux
import re

from function_getMetadata import getAndSaveMetadata
from function_addMetadataAndMaps import addMetadataAndMaps


def runProgram(filename, outputFileName, filenameAndDirectory, iterations, failedFiles, warningFiles, infoMessages, outputFileNameAndDirectory, currentOS, engAudioNoSubs, forceOverwrite, skippedFiles, dryRun):
    wasSkipped = False
    # Check If File Exists
    if forceOverwrite is False:
        if os.path.isfile(outputFileNameAndDirectory):
            if dryRun is False:
                print(Fore.MAGENTA + "All ready exists: " + outputFileName + Fore.RESET)
            skippedFiles += 1
            wasSkipped = True
            return iterations, failedFiles, warningFiles, infoMessages, skippedFiles, wasSkipped  # Skip this loop were done here

    if dryRun is False:

        #print(Fore.BLUE + "Started: " + filename + Fore.RESET)  # Debugging
        overwriteOption = "-n"
        if forceOverwrite is True:
            overwriteOption = "-y"
        iterations += 1  # Log how many files we change

        print(Fore.CYAN + "Started: " + filename + Fore.RESET, end="\r")  # Print and return courser to the start of the line

        try:  # Skip loop if theres a problem with the file
            metadataTable, totalNumOfStreams = getAndSaveMetadata(filename, filenameAndDirectory, currentOS)  # Get metadata
        except:
            failedFiles += 1  # Add to failed count
            iterations -= 1  # Remove from successful count
            return iterations, failedFiles, warningFiles, infoMessages, skippedFiles, wasSkipped

        # Process metadata
        metadataAndMaps, infoMessages = addMetadataAndMaps(filenameAndDirectory, metadataTable, totalNumOfStreams, currentOS, engAudioNoSubs, infoMessages)

        #print("test")
        print(Fore.CYAN + "Started: " + filename + Fore.RESET, end="\r")  # Print and return courser to the start of the line

        # Time for FFmpeg to do its thing:
        if currentOS == "Linux":
            #print("ffmpeg " + overwriteOption + " -v error -xerror -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" +  metadataAndMaps + " -metadata title=\"\" -c copy \"" + outputFileNameAndDirectory + "\"")
            errorCheck = run("ffmpeg " + overwriteOption + " -v error -xerror -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" + metadataAndMaps + " -metadata title=\"\" -c copy \"" + outputFileNameAndDirectory + "\"", capture_output=True, shell=True)
        elif currentOS == "Windows":
            #print("ffmpeg " + overwriteOption + " -v error -xerror -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" + metadataAndMaps + " -metadata title=\"\" -c copy \"" + outputFileNameAndDirectory + "\"")
            errorCheck = run("cmd /c ffmpeg " + overwriteOption + " -v error -xerror -i \"" + filenameAndDirectory + "\" -map_metadata -1 -map_chapters 0" + metadataAndMaps + " -metadata title=\"\" -c copy \"" + outputFileNameAndDirectory + "\"", capture_output=True, shell=True)

        if len(str(errorCheck.stderr)) > 8:  # Integrity and error check
            if str(errorCheck.stderr).find("Referenced QT chapter track not found") != -1:
                print(Fore.CYAN + "Error in the input file, but transcode was completed: " + Fore.GREEN + outputFileName + Fore.RESET)
                infoMessages += 1
                return iterations, failedFiles, warningFiles, infoMessages, skippedFiles, wasSkipped
            elif str(errorCheck.stderr).find("already exists. Exiting.") != -1:
                print("already exists")
                #infoMessages += 1
            elif "unknown timestamp" in str(errorCheck.stderr):
                print(Fore.CYAN + "Error in the input file, but transcode was completed: " + Fore.GREEN + outputFileName + Fore.RESET)
                infoMessages += 1
                return iterations, failedFiles, warningFiles, infoMessages, skippedFiles, wasSkipped
            elif "Non-monotonous DTS" in str(errorCheck.stderr):
                print(Fore.CYAN + "Error in the input file, but transcode was completed: " + Fore.GREEN + outputFileName + Fore.RESET)
                infoMessages += 1
                return iterations, failedFiles, warningFiles, infoMessages, skippedFiles, wasSkipped
            else:
                errorOutput = re.sub("b\"", "", str(errorCheck.stderr))
                errorOutput = re.sub("b\'", "", errorOutput)
                errorOutput = re.sub(r"\\r\\n\'", "", errorOutput)
                errorOutput = re.sub(r"\\r\\n\"", "", errorOutput)
                errorOutput = re.sub(r"\\r\\n", "", errorOutput)
                ffmpegErrors = (errorOutput.replace("[matroska @", "\n[matroska @")).splitlines()
                if len(ffmpegErrors) > 1:
                    del ffmpegErrors[0]  # First index is a newline
                print(Fore.YELLOW + "FFmpeg Error: " + Fore.RESET + ffmpegErrors[0])
                for i in range(1, len(ffmpegErrors)):
                    print("              " + ffmpegErrors[i])
                packingSpaces = ' ' * (len(Fore.BLUE + "Started: " + filename + Fore.RESET) - len(Fore.YELLOW + "May Be Corrupted: " + filename + Fore.RESET))  # Pack the output with spaces or there will be characters left from the overwritten print
                print(Fore.YELLOW + "May Be Corrupted: " + Fore.RESET + filename + Fore.YELLOW + ", so it was not copied" + Fore.RESET + packingSpaces)
                warningFiles += 1
                iterations -= 1  # Remove from successful count
                try:
                    os.remove(Path(outputFileNameAndDirectory))  # Delete the file since its corrupted
                except:
                    print(":o Could not remove: " + outputFileNameAndDirectory)
                return iterations, failedFiles, warningFiles, infoMessages, skippedFiles, wasSkipped

        packingSpaces = " " * (len(Fore.BLUE + "Started: " + filename + Fore.RESET) - len(Fore.GREEN + "Done: " + outputFileName + Fore.RESET))  # Pack the output with spaces or there will be characters left from the overwritten print
        print(Fore.GREEN + "Done: " + outputFileName + Fore.RESET + packingSpaces)

    return iterations, failedFiles, warningFiles, infoMessages, skippedFiles, wasSkipped
