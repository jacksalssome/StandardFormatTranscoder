import os
from pathlib import Path
import shutil
import subprocess
import re
import platform
from pathlib import Path
from colorama import init
from subprocess import run
from colorama import Fore  # Color in windows and linux
import sys
import argparse

from renameFile import renameFile
from runProgram import runProgram

init()  # Stops makes sure windows displays colour

print(
    Fore.YELLOW + "W" + Fore.WHITE + "e" + Fore.GREEN + "l" + Fore.BLUE + "c" + Fore.MAGENTA + "o" + Fore.RED + "m" + Fore.CYAN + "e" + Fore.RESET + " to Standard Format Transcoder")

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help="\"input filename\"")
parser.add_argument('-r', '--recursive', action='store_true', help="Recursively look for files")
args, unknown = parser.parse_known_args()

if unknown:
    print(Fore.YELLOW + "Don't know what this is: " + Fore.RESET + str(unknown))
    print(Fore.YELLOW + "Make sure there are quotes (\"\") around the directory if there are spaces in it." + Fore.RESET)
    input("Press Enter to exit...")
    sys.exit()

if not args.input:  # If not user doesn't input a directory, make sure then run the program in current dir
    print(Fore.YELLOW + "No Directory was inputted, do you want to run in the current directory:" + Fore.RESET)
    print(str(os.path.dirname(os.path.realpath(__file__))) + Fore.YELLOW + "? [Y/N]" + Fore.RESET)  # Ask the user if they want to use current dir
    answerYN = None
    while answerYN not in ("yes", "no", "y", "n"):
        answerYN = input()
        if answerYN == "yes" or answerYN == "y":
            directory = os.path.dirname(os.path.realpath(__file__))  # Set working dir to programs dir
        elif answerYN == "no" or answerYN == "n":
            sys.exit()
        else:
            print("Please enter yes or no.")
elif os.path.exists(args.input):
    directory = args.input  # Set working dir to input dir
    if os.path.isfile(directory):  # If user puts in a link to a single file
        print(Fore.YELLOW + "Cant handle direct files, only the directory they are in." + Fore.RESET)
        print(Fore.YELLOW + "Would you like to covert all files in this directory: " + Fore.RESET + "\"" + os.path.dirname(directory) + "\"" + Fore.YELLOW + "? [Y/N]" + Fore.RESET)
        answerYN = None
        while answerYN not in ("yes", "no", "y", "n"):
            answerYN = input()
            if answerYN == "yes" or answerYN == "y":
                directory = os.path.dirname(directory)  # Trim input dir to the dir of the inputted file
            elif answerYN == "no" or answerYN == "n":
                sys.exit()
            else:
                print("Please enter yes or no.")
else:
    print(Fore.YELLOW + "Can't find file path: " + Fore.RESET + args.input)
    input("Press Enter to exit...")
    sys.exit()

runRecursive = False

if args.recursive is not None:  # If -r or --recursive is present then enable recursive
    runRecursive = True
elif args.recursive is None:
    runRecursive = False

# print(platform.system())

# print(os.listdir(directory))

iterations = 0
failedFiles = 0
warningFiles = 0

if runRecursive == True:
    for root, dirs, files in os.walk(directory):  # find the root, the directories and files.
        for filename in files:  # Iterate over every file
            if filename.endswith(".mkv"):  # If current file is an MKV
                if root.find("SFT output") != -1:  # stop from descending into own output
                    continue

                directory = str(Path(directory).parent)

                outputFileName = renameFile(filename)  # Call up function renameFile
                outputFileNameTmp = os.path.join(root) + "\\" + outputFileName  # Rename File and put it in "SFT output; <Selected folder>" directory
                # Make the top directory "SFT output; <Selected folder>":
                Path((os.path.join(root)).replace(directory, directory + "\\" + "SFT output; ")).mkdir(parents=True, exist_ok=True)
                # Add "SFT output; <Selected folder>" as a top directory and we will create a clone directory of only (.mkv's):
                outputFileNameTmp = outputFileNameTmp.replace(directory, directory + "\\" + "SFT output; ")  # Absolute path of output file
                filenameAndDirectory = os.path.join(root) + "\\" + filename  # Absolute path of input file
                try:
                    iterations, failedFiles, warningFiles = runProgram(filename, outputFileName, filenameAndDirectory, iterations, failedFiles, warningFiles, outputFileNameTmp)
                except KeyboardInterrupt:  # Handling CTRL+C
                    print("")  # Dealing with the end='/r' in runProgram
                    print("CTRL+C pressed, Exiting...")
                    os.remove(Path(outputFileNameTmp))  # Delete the file since its not done
                    sys.exit()
                except:  # if runProgram gives us an error or warning well jump to the next file
                    continue

elif runRecursive == False:
    for filename in os.listdir(directory):
        if filename.endswith(".mkv"):  # Find Any MKV files
            outputFileName = renameFile(filename)  # Rename File
            outputFileNameAndDirectory = directory + "\\" + "SFT output" + "\\" + outputFileName  # Where to put the output file
            filenameAndDirectory = directory + "\\" + filename  # Absolute path of input file
            try:
                iterations, failedFiles, warningFiles = runProgram(filename, outputFileName, filenameAndDirectory, iterations, failedFiles, warningFiles, outputFileNameAndDirectory)
            except KeyboardInterrupt:  # Handling CTRL+C
                print("")  # Dealing with the end='/r' in runProgram
                print("CTRL+C pressed, Exiting...")
                os.remove(Path(outputFileNameAndDirectory))  # Delete the file since its not done
                sys.exit()
            except:  # if runProgram gives us an error or warning well jump to the next file
                continue

# Info on number of files processed, warnings and errors
if iterations != 0:
    print("Finished", iterations, "files")
elif iterations == 0:
    print("No Files Found")
if failedFiles != 0:
    print(Fore.RED + str(failedFiles) + " Failed" + Fore.RESET)
if warningFiles != 0:
    print(Fore.YELLOW + str(warningFiles) + " Warnings" + Fore.RESET)
input("Press ENTER to exit...")

