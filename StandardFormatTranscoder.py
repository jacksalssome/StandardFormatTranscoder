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
from runProgram import runProgram

init()  # Stops makes sure windows displays colour

print(
    Fore.YELLOW + "W" + Fore.WHITE + "e" + Fore.GREEN + "l" + Fore.BLUE + "c" + Fore.MAGENTA + "o" + Fore.RED + "m" + Fore.CYAN + "e" + Fore.RESET + " to Standard Format Transcoder")

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="\"input filename\"")
parser.add_argument('-r', '--recursive', action='store_true', help="Recursively look for files")
args, unknown = parser.parse_known_args()

if unknown:
    print(Fore.YELLOW + "Don't know what this is: " + Fore.RESET + str(unknown))
    print(Fore.YELLOW + "Make sure there are quotes (\"\") around the directory if there are spaces in it." + Fore.RESET)
    input("Press Enter to exit...")
    sys.exit()

if not args.input:  # If not user doesn't input a directory, make sure then run the program in current dir
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

runRecursive = False

if args.recursive is not None:
    runRecursive = True
elif args.recursive is None:
    runRecursive = False

# print(platform.system())

# print(os.listdir(directory))

# print("Transcode Starting")
Path(directory + "\\" + "MKVoutput").mkdir(parents=True, exist_ok=True)
# Path("Metadata/").mkdir(parents=True, exist_ok=True)

iterations = 0
failedFiles = 0
warningFiles = 0

if runRecursive == True:
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".mkv"):  # Find Any MKV files
                outputFileName = renameFile(filename)
                outputFileNameTmp = os.path.join(root) + "\\" + outputFileName  # Rename File and put it in MKVoutput directory
                justTheRoot = os.path.join(root)

                Path(justTheRoot.replace(directory, directory + "\\" + "MKVoutput")).mkdir(parents=True, exist_ok=True)

                outputFileNameTmp = outputFileNameTmp.replace(directory, directory + "\\" + "MKVoutput")  # Add MKVoutput into the directory to create a clone

                outputFileNameAndDirectory = outputFileNameTmp

                filenameAndDirectory = os.path.join(root) + "\\" + filename  # Absoulte path to file

                try:
                    iterations, failedFiles, warningFiles = runProgram(filename, outputFileName, filenameAndDirectory, iterations, failedFiles, warningFiles, outputFileNameAndDirectory)
                except KeyboardInterrupt:
                    print("")
                    print("CTRL+C pressed, Exiting...")
                    os.remove(Path(outputFileNameAndDirectory))  # Delete the file since its not done
                    sys.exit()
                except:
                    continue

elif runRecursive == False:
    for filename in os.listdir(directory):
        if filename.endswith(".mkv"):  # Find Any MKV files
            outputFileNameAndDirectory = directory + "\\" + "MKVoutput" + "\\" + renameFile(filename)  # Rename File and put it in MKVoutput directory
            outputFileName = renameFile(filename)
            filenameAndDirectory = directory + "\\" + filename  # Absoulte path to file
            try:
                iterations, failedFiles, warningFiles = runProgram(filename, outputFileName, filenameAndDirectory, iterations, failedFiles, warningFiles, outputFileNameAndDirectory)
            except KeyboardInterrupt:
                print("")
                print("CTRL+C pressed, Exiting...")
                os.remove(Path(outputFileNameAndDirectory))  # Delete the file since its not done
                sys.exit()
            except:
                continue

if iterations != 0:
    print("Finished", iterations, "files")
elif iterations == 0:
    print("No Files Found")
if failedFiles != 0:
    print(Fore.RED + str(failedFiles) + " Failed" + Fore.RESET)
if warningFiles != 0:
    print(Fore.YELLOW + str(warningFiles) + " Warnings" + Fore.RESET)
input("Press ENTER to exit...")

