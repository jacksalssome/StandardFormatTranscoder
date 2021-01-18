import subprocess
import re


def compareSizes(streamNum, filename, currentOS):

    #print("Determining best subtitle stream")

    valOne = 0
    output = ""

    # Found on stackoverflow, just streams out packets then i capture then in a list
    if currentOS == "Linux":
        output = str(subprocess.check_output("ffprobe -v error -show_packets -select_streams " + str(streamNum) + " -show_entries packet=size -of default=nokey=1:noprint_wrappers=1 \"" + filename + "\"", shell=False))
    elif currentOS == "Windows":
        output = str(subprocess.check_output("cmd /c ffprobe -v error -show_packets -select_streams "+str(streamNum)+" -show_entries packet=size -of default=nokey=1:noprint_wrappers=1 \""+filename+"\"", shell=False))

    cleanOutput = re.sub("[b']", "", output)
    cleanOutput = cleanOutput.replace("\\r", "")

    # Sum up packets for the final value in Bytes (its not 100% correct)

    myList = cleanOutput.split('\\n')

    for line in myList:
        #print(line)
        if not line == "":
            valOne += int(line)

    #print(valOne)
    #print(sum(myList))

    #print(cleanOut)
    #print("Stream "+str(streamNum)+": "+str(f'{valOne:,}')+" Bytes")

    return valOne
