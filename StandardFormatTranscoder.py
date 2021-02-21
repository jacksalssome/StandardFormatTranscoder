import os
from os.path import basename
from pathlib import Path
import re
import platform
from colorama import init
from colorama import Fore  # Color in Windows and Linux
import sys
from subprocess import run
import subprocess
import argparse
# Local Files
from function_renameFile import renameFile
from function_runProgram import runProgram
from function_filePathCheck import filePathCheck, checkIfPathIsAFile

# TODO:
# Add --Keep "Audio Subtitles Video Attachments"

#Note
# Try to keep outputs to terminal/console below 120 characters

init()  # Makes sure windows displays colour. --KEEP AT TOP--

# Check Platform, set file path slashes
if platform.system() == "Linux":
    fileSlashes = "/"
    currentOS = "Linux"
elif platform.system() == "Windows":
    fileSlashes = "\\"
    currentOS = "Windows"
else:
    print(Fore.RED + "Unsupported operating system :(" + Fore.RESET)
    input("Press Enter to exit...")
    sys.exit()
# Check for FFmpeg
try:
    run("ffmpeg", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except:
    print(Fore.RED + "FFmpeg Is Not Installed :(" + Fore.RESET)
    print(Fore.RED + "sudo apt install ffmpeg" + Fore.RESET)
    print(Fore.RED + "sudo dnf install ffmpeg" + Fore.RESET)
    input("Press Enter to exit...")
    sys.exit()

inputDirectory, outputDirectory = "", ""
runRecursive, runRename, engAudioNoSubs, forceOverwrite, noDirInputted, dryRun = False, False, False, False, False, False

print(Fore.YELLOW + "W" + Fore.WHITE + "e" + Fore.GREEN + "l" + Fore.BLUE + "c" + Fore.MAGENTA + "o" + Fore.RED + "m" + Fore.CYAN + "e" + Fore.RESET + " to Standard Format Transcoder, by Jacksalssome")

parser = argparse.ArgumentParser()
parser.add_argument('--overwrite', action='store_true', help="Overwrites files if they already exist")
parser.add_argument('-i', '--input', help="input directory")
parser.add_argument('-o', '--output', help="output directory")
parser.add_argument('-r', '--recursive', action='store_true', help="Recursively look for files")
parser.add_argument('--rename', action='store_true', help="Use the auto rename function")
parser.add_argument('--engAudioNoSubs', action='store_true', help="Use the auto rename function")
parser.add_argument('--DryRun', action='store_true', help="Runs without changing files")
args, unknown = parser.parse_known_args()

if unknown:  # This is wildly complicated for just an error message, but it's art.
    tempString = re.sub(",", Fore.YELLOW + "," + Fore.RESET, (re.sub("\'", Fore.YELLOW + "\"" + Fore.RESET, (re.sub("(\[')|('])", "", str(unknown))))))
    if "," + Fore.RESET in tempString:
        tempString = Fore.YELLOW + "these are: \"" + Fore.RESET + tempString  # This is all to be grammatically correct.
    else:
        tempString = Fore.YELLOW + "this is: \"" + Fore.RESET + tempString
    print(Fore.YELLOW + "Don't know what " + Fore.RESET + tempString + Fore.YELLOW + "\"" + Fore.RESET)
    print(Fore.YELLOW + "Make sure there are quotes (\"\") around the input and output directory's if there are spaces in it." + Fore.RESET)
    input("Press Enter to exit...")
    sys.exit()

# Check if Inputs and Outputs are present
if not args.input and not args.output:  # Both missing
    # Check that were not in the root of a drive
    if args.input is not None:
        inputArg = args.input
        filePathCheck(currentOS, inputArg)
    print(Fore.YELLOW + "No input or output Directory was inputted, do you want to transcode files in:" + Fore.RESET)
    print(str(os.path.dirname(os.path.realpath(__file__))) + Fore.YELLOW + "? [Y/N]" + Fore.RESET)  # Ask the user if they want to use current dir
    answerYN = None
    while answerYN not in ("yes", "no", "y", "n"):
        answerYN = input()
        if answerYN == "yes" or answerYN == "y":
            inputDirectory = os.path.dirname(os.path.realpath(__file__))  # Set input dir to programs dir
            outputDirectory = os.path.dirname(os.path.realpath(__file__))  # Set output dir to programs dir
            noDirInputted = True  # So we make a copy of the directory
        elif answerYN == "no" or answerYN == "n":
            sys.exit()
        else:
            print("Please enter yes or no.")
elif not args.input:  # Input missing
    print(Fore.YELLOW + "No input Directory was inputted, do you want to transcode files from:" + Fore.RESET)
    print(str(os.path.dirname(os.path.realpath(__file__))) + Fore.YELLOW + "? [Y/N]" + Fore.RESET)  # Ask the user if they want to use current dir
    answerYN = None
    while answerYN not in ("yes", "no", "y", "n"):
        answerYN = input()
        if answerYN == "yes" or answerYN == "y":
            inputDirectory = os.path.dirname(os.path.realpath(__file__))  # Set working dir to programs dir
        elif answerYN == "no" or answerYN == "n":
            sys.exit()
        else:
            print("Please enter yes or no.")
elif not args.output:  # Output missing
    print(Fore.YELLOW + "No output Directory was inputted, do you want to transcode files to:" + Fore.RESET)
    print(str(os.path.dirname(os.path.realpath(__file__))) + Fore.YELLOW + "? [Y/N]" + Fore.RESET)  # Ask the user if they want to use current dir
    answerYN = None
    while answerYN not in ("yes", "no", "y", "n"):
        answerYN = input()
        if answerYN == "yes" or answerYN == "y":
            outputDirectory = os.path.dirname(os.path.realpath(__file__))  # Set working dir to programs dir
        elif answerYN == "no" or answerYN == "n":
            sys.exit()
        else:
            print("Please enter yes or no.")

# ---- Input ----
if args.input is not None:
    if os.path.exists(args.input):
        inputDirectory = args.input  # Set working dir to input dir
        typeOfDirectory = "input"
        checkIfPathIsAFile(inputDirectory, typeOfDirectory)
    else:
        print(Fore.YELLOW + "Can't find input file path: \"" + Fore.RESET + args.input + Fore.YELLOW + "\"" + Fore.RESET)
        input("Press Enter to exit...")
        sys.exit()
# ---- Output ----
if args.output is not None:
    if os.path.exists(args.output):
        outputDirectory = args.output  # Set working dir to input dir
        typeOfDirectory = "output"
        checkIfPathIsAFile(outputDirectory, typeOfDirectory)
    else:
        print(Fore.YELLOW + "Can't find output file path: \"" + Fore.RESET + args.output + Fore.YELLOW + "\"" + Fore.RESET)
        print(Fore.YELLOW + "Note: this program doesn't create directories" + Fore.RESET)
        input("Press Enter to exit...")
        sys.exit()

if args.engAudioNoSubs is True:  # If -r or --recursive is present then enable recursive
    engAudioNoSubs = True
if args.overwrite is True:  # If -r or --recursive is present then enable recursive
    forceOverwrite = True
if args.recursive is True:  # If -r or --recursive is present then enable recursive
    runRecursive = True
if args.rename is True:  # If --rename present, then enable auto renaming
    runRename = True
if args.DryRun is True:
    dryRun = True

# print(os.listdir(inputDirectory))

iterations, failedFiles, warningFiles, infoMessages, skippedFiles, tempIterations = 0, 0, 0, 0, 0, 0

if runRecursive is True:
    parentDirectoryName = basename(inputDirectory)
    if noDirInputted is True:
        outputDirectory = str(Path(inputDirectory).parent) + fileSlashes + "SFT output of; " + parentDirectoryName
    previousRelativeInput = ""
    previousOutputFilename = ""
    for root, dirs, files in os.walk(inputDirectory):  # find the root, the directories and files.
        skipThis = False
        for currentDir in dirs:  # Stop the Snake from eating its tail (Preventing recursion into own output is user is outputting to a directory in the input directory)
            #print(outputDirectory + " ... " + root)
            if root.find(outputDirectory) != -1:  # stop from descending into own output
                #print("Skip")
                skipThis = True
                continue
        if skipThis is True:
            #print("Skipping")
            continue
        for inputFilename in files:  # Iterate over every file
            if inputFilename.endswith(".mkv") or inputFilename.endswith(".mp4") or inputFilename.endswith(".m4v"):  # If current file is an MKV, MP4 or M4V
                inputDirectory = inputDirectory
                inputFilenameAndDirectory = root + fileSlashes + inputFilename  # Absolute path of input file
                if runRename is True:
                    outputFilename = renameFile(currentOS, inputFilenameAndDirectory, inputFilename, previousOutputFilename, dryRun)  # Call up function renameFile | Don't have to mess with extension because the function does it.
                else:
                    outputFilename = inputFilename[:-4] + ".mkv"  # Remove last 4 characters = .m4v or .mp4, etc and replace with .mkv
                outputFilenameAndDirectory = root.replace(inputDirectory, outputDirectory) + fileSlashes + outputFilename
                if dryRun is False:
                    Path(root.replace(inputDirectory, outputDirectory)).mkdir(parents=True, exist_ok=True)
                try:
                    iterations, failedFiles, warningFiles, infoMessages, skippedFiles, wasSkipped = runProgram(inputFilename, outputFilename, inputFilenameAndDirectory, iterations, failedFiles, warningFiles, infoMessages, outputFilenameAndDirectory, currentOS, engAudioNoSubs, forceOverwrite, skippedFiles, dryRun)
                    if dryRun is True:
                        relativeInput = inputFilenameAndDirectory.replace(inputDirectory, "")
                        relativeOutput = outputFilenameAndDirectory.replace(outputDirectory, "")
                        if tempIterations == 0:
                            print("")
                            print(Fore.CYAN + inputFilenameAndDirectory.replace(relativeInput, "") + "\\" + Fore.MAGENTA + " ---> " + Fore.CYAN + outputFilenameAndDirectory.replace(relativeOutput, "") + "\\" + Fore.RESET)
                            tempIterations += 1
                        indentNum = 1
                        for i in relativeInput:
                            slash = relativeInput.find("\\")
                            relativeInput = relativeInput[slash + 1:len(relativeInput) + 2]
                            if previousRelativeInput.find(relativeInput[0:relativeInput.find("\\")]) == -1 and relativeInput.find("\\") != -1:
                                #print("TRUE")
                                print(Fore.CYAN + "    " * indentNum + relativeInput[0:relativeInput.find("\\")] + Fore.RESET)
                            elif relativeInput.find("\\") == -1:
                                if wasSkipped is False:
                                    if runRename is True:
                                        print("    " * indentNum + inputFilename + Fore.MAGENTA + " ---> " + Fore.RESET + outputFilename)
                                    if runRename is False:
                                        print("    " * indentNum + inputFilename)
                                    iterations += 1
                                elif wasSkipped is True:
                                    print("    " * indentNum + Fore.MAGENTA + outputFilename + " (Already Exists)" + Fore.RESET)
                                break
                            indentNum += 1
                        previousRelativeInput = inputFilenameAndDirectory.replace(inputDirectory, "")
                        #print(dryRunInputFile + Fore.CYAN + " --> " + Fore.RESET + dryRunOutputFile)
                    previousOutputFilename = outputFilename[:-4]  # For renameFile
                except KeyboardInterrupt:  # Handling CTRL+C
                    print("")  # Dealing with the end='/r' in runProgram
                    print("CTRL+C pressed, Exiting...")
                    os.remove(Path(outputFilenameAndDirectory))  # Delete the file since its not completed
                    sys.exit()
                #except:  # if runProgram gives us an error or warning well jump to the next file
                    #print("Error #1")
                    #continue
    if dryRun is False:
        print(Fore.CYAN + "Your files are in: \"" + Fore.RESET + outputDirectory + fileSlashes + Fore.CYAN + "\"" + Fore.RESET)  # Program is almost done, so we'll make sure the user knows where their files are.

elif runRecursive is False:
    previousOutputFilename = ""
    for inputFilename in os.listdir(inputDirectory):
        if inputFilename.endswith(".mkv") or inputFilename.endswith(".mp4") or inputFilename.endswith(".m4v"):  # Find Any MKV files
            inputFilenameAndDirectory = inputDirectory + fileSlashes + inputFilename  # Absolute path of input file
            if runRename is True:  # Rename File
                outputFilename = renameFile(currentOS, inputFilenameAndDirectory, inputFilename, previousOutputFilename, dryRun)  # Call up function renameFile
            else:  # keep file name
                outputFilename = inputFilename[:-4] + ".mkv"  # Replace extension with .mkv
            if noDirInputted is True:
                outputFileNameAndDirectory = inputDirectory + fileSlashes + "SFT output" + fileSlashes + outputFilename  # Where to put the output file
                if dryRun is False:
                    Path(inputDirectory + fileSlashes + "SFT output" + fileSlashes).mkdir(parents=True, exist_ok=True)  # Make Dir
            elif noDirInputted is False:
                outputFileNameAndDirectory = outputDirectory + fileSlashes + outputFilename
            try:
                iterations, failedFiles, warningFiles, infoMessages, skippedFiles, wasSkipped = runProgram(inputFilename, outputFilename, inputFilenameAndDirectory, iterations, failedFiles, warningFiles, infoMessages, outputFileNameAndDirectory, currentOS, engAudioNoSubs, forceOverwrite, skippedFiles, dryRun)
                if dryRun is True and wasSkipped is False:
                    if runRename is True:
                        print("-   " + inputFilename + Fore.MAGENTA + " ---> " + Fore.RESET + outputFilename)
                        iterations += 1
                    elif runRename is False:
                        print("-   " + inputFilename)
                        iterations += 1
                elif dryRun is True:
                    print("    " + Fore.MAGENTA + outputFilename + " (Already Exists)" + Fore.RESET)
                previousOutputFilename = outputFilename[:-4]  # For renameFile
            except KeyboardInterrupt:  # Handling CTRL+C
                print("")  # Dealing with the end='/r' in runProgram
                print("CTRL+C pressed, Exiting...")
                os.remove(Path(outputFileNameAndDirectory))  # Delete the file since its not done
                sys.exit()

# Info on number of files processed, warnings and errors
if iterations != 0:
    if dryRun is True:
        print(Fore.CYAN + "There would be", iterations, "files changed" + Fore.RESET)
    else:
        print(Fore.CYAN + "Finished", iterations, "files" + Fore.RESET)
if skippedFiles != 0:
    print(Fore.CYAN + "Skipped", skippedFiles, "files" + Fore.RESET)
if infoMessages != 0:
    print(Fore.CYAN + str(infoMessages) + " Info Messages" + Fore.RESET)
if failedFiles != 0:
    print(Fore.RED + str(failedFiles) + " Failed" + Fore.RESET)
if warningFiles != 0:
    print(Fore.YELLOW + str(warningFiles) + " Warnings" + Fore.RESET)
elif skippedFiles == 0 and warningFiles == 0 and failedFiles == 0 and iterations == 0:
    print("No Files found")
input("Press ENTER to exit...")
