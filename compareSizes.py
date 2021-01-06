import subprocess
import re
import ffmpeg
import json

iterations = 0
def compareSizes(streamNum, filename):

    #print("Determining best subtitle via stream filesize")

    valOne = 0

    # Found on stackoverflow, just streams out packets then i capture then in a list
    output = str(subprocess.check_output("cmd /c ffprobe -v error -show_packets -select_streams "+str(streamNum)+" -show_entries packet=size -of default=nokey=1:noprint_wrappers=1 \""+filename+"\"", shell=False))

    cleanOutput = re.sub("[b']", "", output)
    cleanOutput = cleanOutput.replace("\\r", "")

    # Sum up packets for the final value in Bytes (its not 100% correct)

    myList = cleanOutput.split('\\n')

    for line in myList:
        #print(line)
        if line != "":
            valOne += int(line)

    #print(valOne)
    #print(sum(myList))

    #print(cleanOut)
    #print("Stream "+str(streamNum)+": "+str(f'{valOne:,}')+" Bytes")

    return valOne

