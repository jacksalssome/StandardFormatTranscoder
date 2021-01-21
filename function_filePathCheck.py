from colorama import Fore
import sys
import re
import os


def filePathCheck(currentOS, inputArg):
    if currentOS == "Windows" and len(inputArg) <= 3:  # <= 3 equals C:\ (root dir)
        print(Fore.YELLOW + "Can't run in root of drive, input has to be like: " + Fore.RESET + "-i \"D:\\folder\"")
    elif currentOS == "Windows" and len(inputArg) <= 4 and re.search("[A-Z][A-Z]:\\\\", str(inputArg)):  # <= 4 equals AB:\ (root dir)
        print(Fore.YELLOW + "Nice drive letters, but can't run in root of drive, input has to be like: " + Fore.RESET + "-i \"D:\\folder\"")
    elif currentOS == "Linux" and len(inputArg) <= 1:  # <= 2 equals / (root dir)
        print(Fore.YELLOW + "Can't run in root of drive, input has to be like: " + Fore.RESET + "-i \"/home\"")
    else:
        print(Fore.YELLOW + "Can't find file path: \"" + Fore.RESET + inputArg + Fore.YELLOW + "\"" + Fore.RESET)
        print(Fore.YELLOW + "Note: this program doesn't create directories" + Fore.RESET)
    input("Press Enter to exit...")
    sys.exit()


def checkIfPathIsAFile(Directory, typeOfDirectory):
    if os.path.isfile(Directory):  # If user puts in a link to a single file
        if typeOfDirectory == "input":
            print(Fore.YELLOW + "Cant handle direct files, only the directory they are in." + Fore.RESET)
            print(Fore.YELLOW + "Would you like to use this directory: " + Fore.RESET + "\"" + os.path.dirname(Directory) + "\"" + Fore.YELLOW + "? [Y/N]" + Fore.RESET)
        elif typeOfDirectory == "output":
            print(Fore.YELLOW + "Output to a single file, only to a directory." + Fore.RESET)
            print(Fore.YELLOW + "Would you like to output to this directory: " + Fore.RESET + "\"" + os.path.dirname(Directory) + "\"" + Fore.YELLOW + "? [Y/N]" + Fore.RESET)
        else:
            breakpoint()
        answerYN = None
        while answerYN not in ("yes", "no", "y", "n"):
            answerYN = input()
            if answerYN == "yes" or answerYN == "y":
                Directory = os.path.dirname(Directory)  # Trim input dir to the dir of the inputted file
            elif answerYN == "no" or answerYN == "n":
                sys.exit()
            else:
                print("Please enter yes or no.")
    return Directory
