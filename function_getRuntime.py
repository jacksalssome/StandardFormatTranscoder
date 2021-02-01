import subprocess
from decimal import Decimal
from colorama import Fore


def getRuntime(currentOS, filenameAndDirectory, filename):
    try:
        if currentOS == "Linux":
            runTime = subprocess.check_output("ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"" + filenameAndDirectory + "\"", shell=False)  # runtime in minutes
        if currentOS == "Windows":
            runTime = subprocess.check_output("cmd /c ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"" + filenameAndDirectory + "\"", shell=False)
    except:
        print(Fore.YELLOW + ":( Couldn't get runtime for: \"" + Fore.RESET + filename + Fore.YELLOW + "\"" + Fore.RESET)
        return None

    #print("")
    #print(runTime)

    return int(Decimal(str(runTime).replace("b\'", "").replace("\'", "").replace(r"\r\n", "")))