from colorama import Fore
import argparse


def filePathCheck(currentOS, input, args.input):
    if currentOS == "Windows" and len(args.input) <= 3:  # <= 3 equals C:\ (root dir)
        print(Fore.YELLOW + "Can't run in root of drive, input has to be like: " + Fore.RESET + "-i \"D:\\folder\"")
    elif currentOS == "Windows" and len(args.input) <= 4 and re.search("[A-Z][A-Z]:\\\\", str(args.input)):  # <= 4 equals AB:\ (root dir)
        print(Fore.YELLOW + "Nice drive letters, but can't run in root of drive, input has to be like: " + Fore.RESET + "-i \"D:\\folder\"")
    elif currentOS == "Linux" and len(args.input) <= 1:  # <= 2 equals / (root dir)
        print(Fore.YELLOW + "Can't run in root of drive, input has to be like: " + Fore.RESET + "-i \"/home\"")
    else:
        print(Fore.YELLOW + "Can't find file path: \"" + Fore.RESET + args.input + Fore.YELLOW + "\"" + Fore.RESET)
        print(Fore.YELLOW + "Note: this program doesn't create directories" + Fore.RESET)
    input("Press Enter to exit...")
    sys.exit()