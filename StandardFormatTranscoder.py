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
from renameFile import renameFile
from runProgram import runProgram


init()  # Makes sure windows displays colour. KEEP AT TOP

# Check Platform
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
    print(Fore.RED + "FFmpeg Is Not Installed :(" + Fore.RESET)  # Parent function is runProgram, so gotta pack it.
    input("Press Enter to exit...")
    sys.exit()

# TODO:
# Add -o --output, so user can specify and output dir
# Add MP4?

print(Fore.YELLOW + "W" + Fore.WHITE + "e" + Fore.GREEN + "l" + Fore.BLUE + "c" + Fore.MAGENTA + "o" + Fore.RED + "m" + Fore.CYAN + "e" + Fore.RESET + " to Standard Format Transcoder")

parser = argparse.ArgumentParser()
parser.add_argument('--force', action='store_true', help="\"Force Overwrite\"")
parser.add_argument('-i', '--input', help="\"input filename\"")
parser.add_argument('-r', '--recursive', action='store_true', help="Recursively look for files")
parser.add_argument('--rename', action='store_true', help="Use the auto rename function")
parser.add_argument('--engAudioNoSubs', action='store_true', help="Use the auto rename function")
args, unknown = parser.parse_known_args()

if unknown:  # This is wildly complicated for just an error message, but it's art.
    tempString = re.sub(",", Fore.YELLOW + "," + Fore.RESET, (re.sub("\'", Fore.YELLOW + "\"" + Fore.RESET, (re.sub("(\[')|('\])", "", str(unknown))))))
    if "," + Fore.RESET in tempString:
        tempString = Fore.YELLOW + "these are: \"" + Fore.RESET + tempString
    else:
        tempString = Fore.YELLOW + "this is: \"" + Fore.RESET + tempString
    print(Fore.YELLOW + "Don't know what " + Fore.RESET + tempString + Fore.YELLOW + "\"" + Fore.RESET)
    print(Fore.YELLOW + "Make sure there are quotes (\"\") around the input and output directory's if there are spaces in it." + Fore.RESET)
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
    if currentOS == "Windows" and len(args.input) <= 3:  # <= 3 equals C:\ (root dir)
            print(Fore.YELLOW + "Can't run in root of drive, input has to be like: " + Fore.RESET + "-i \"D:\\folder\"")
    elif currentOS == "Windows" and len(args.input) <= 4 and re.search("[A-Z][A-Z]:\\", str(args.input)):  # <= 4 equals AB:\ (root dir)
            print(Fore.YELLOW + "Nice drive letters, but can't run in root of drive, input has to be like: " + Fore.RESET + "-i \"D:\\folder\"")
    elif currentOS == "Linux" and len(args.input) <= 1:  # <= 2 equals / (root dir)
            print(Fore.YELLOW + "Can't run in root of drive, input has to be like: " + Fore.RESET + "-i \"/home\"")
    else:
        print(Fore.YELLOW + "Can't find file path: \"" + Fore.RESET + args.input + Fore.YELLOW + "\"" + Fore.RESET)
    input("Press Enter to exit...")
    sys.exit()


if args.engAudioNoSubs == True:  # If -r or --recursive is present then enable recursive
    engAudioNoSubs = True
elif args.engAudioNoSubs == False:
    engAudioNoSubs = False

if args.force == True:  # If -r or --recursive is present then enable recursive
    forceOverwrite = True
elif args.force == False:
    forceOverwrite = False

if args.recursive == True:  # If -r or --recursive is present then enable recursive
    runRecursive = True
elif args.recursive == False:
    runRecursive = False

if args.rename == True:  # If --rename present, then enable auto renaming
    runRename = True
elif args.rename == False:
    runRename = False

# print(os.listdir(directory))

iterations = 0
failedFiles = 0
warningFiles = 0
infos = 0

if runRecursive == True:
    parentDirectoryName = basename(directory)
    outputDirectory = str(Path(directory).parent) + fileSlashes + "SFT output of; " + parentDirectoryName
    for root, dirs, files in os.walk(directory):  # find the root, the directories and files.
        for inputFilename in files:  # Iterate over every file
            if inputFilename.endswith(".mkv") or inputFilename.endswith(".mp4") or inputFilename.endswith(".m4v"):  # If current file is an MKV, MP4 or M4V
                if root.find("SFT output of; " + parentDirectoryName) != -1:  # stop from descending into own output
                    continue

                inputDirectory = directory
                inputFilenameAndDirectory = root + fileSlashes + inputFilename  # Absolute path of input file
                if runRename == True:
                    outputFilename = renameFile(inputFilename)  # Call up function renameFile | Don't have to mess with extension because the function does it.
                else:
                    outputFilename = inputFilename[:-4] + ".mkv"  # Remove last 4 characters = .m4v or .mp4, etc and replace with .mkv
                outputFilenameAndDirectory = root.replace(directory, outputDirectory) + fileSlashes + outputFilename  # Rename File and put it in "SFT output; <Selected folder>" directory

                # Make the top directory "SFT output; <Selected folder>":
                Path(root.replace(directory, outputDirectory)).mkdir(parents=True, exist_ok=True)

                try:
                    iterations, failedFiles, warningFiles = runProgram(inputFilename, outputFilename, inputFilenameAndDirectory, iterations, failedFiles, warningFiles, infos, outputFilenameAndDirectory, currentOS, engAudioNoSubs, forceOverwrite)
                except KeyboardInterrupt:  # Handling CTRL+C
                    print("")  # Dealing with the end='/r' in runProgram
                    print("CTRL+C pressed, Exiting...")
                    os.remove(Path(outputFilenameAndDirectory))  # Delete the file since its not completed
                    sys.exit()
                except:  # if runProgram gives us an error or warning well jump to the next file
                    continue
    print(Fore.CYAN + "Your files are in: \"" + Fore.RESET + outputDirectory + fileSlashes + Fore.CYAN + "\"" + Fore.RESET)  # Program is almost done, so we'll make sure the user knows where their files are.

elif runRecursive == False:
    for inputFilename in os.listdir(directory):
        if inputFilename.endswith(".mkv") or inputFilename.endswith(".mp4") or inputFilename.endswith(".m4v"):  # Find Any MKV files
            Path(directory + fileSlashes + "SFT output" + fileSlashes).mkdir(parents=True, exist_ok=True)  # Make Dir

            if runRename == True:  # Rename File
                outputFilename = renameFile(inputFilename)  # Call up function renameFile
            else:  # keep file name
                outputFilename = inputFilename[:-4] + ".mkv"  # Replace extension with .mkv

            outputFileNameAndDirectory = directory + fileSlashes + "SFT output" + fileSlashes + outputFilename  # Where to put the output file
            inputFilenameAndDirectory = directory + fileSlashes + inputFilename  # Absolute path of input file
            try:
                iterations, failedFiles, warningFiles = runProgram(inputFilename, outputFilename, inputFilenameAndDirectory, iterations, failedFiles, warningFiles, infos, outputFileNameAndDirectory, currentOS, engAudioNoSubs, forceOverwrite)
            except KeyboardInterrupt:  # Handling CTRL+C
                print("")  # Dealing with the end='/r' in runProgram
                print("CTRL+C pressed, Exiting...")
                os.remove(Path(outputFileNameAndDirectory))  # Delete the file since its not done
                sys.exit()
            except:  # if runProgram gives us an error or warning well jump to the next file
                continue

# Info on number of files processed, warnings and errors
if iterations != 0:
    print(Fore.CYAN + "Finished", iterations, "files" + Fore.RESET)

if infos != 0:
    print(Fore.RED + str(infos) + " Info's" + Fore.RESET)
if failedFiles != 0:
    print(Fore.RED + str(failedFiles) + " Failed" + Fore.RESET)
if warningFiles != 0:
    print(Fore.YELLOW + str(warningFiles) + " Warnings" + Fore.RESET)
input("Press ENTER to exit...")
