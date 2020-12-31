import subprocess
import re

def compareSizes(streamNum, filename):
    valOne = 0

    output = str(subprocess.check_output("cmd /c ffprobe -v error -show_packets -select_streams "+str(streamNum)+" -show_entries packet=size -of default=nokey=1:noprint_wrappers=1 \""+filename+"\"", shell=False))

    #os.system("cmd /c ffprobe -v error -show_packets -select_streams s:1 -show_entries packet=size -of default=nokey=1:noprint_wrappers=1 \""+filename+"\" > \"Metadata\\" + filename + "(Size2).txt\" 2>&1")

    #txtfile = open("Metadata\\" + filename + "(Size2).txt", encoding="utf8")

    cleanOutput = re.sub("[b']", "", output)
    cleanOutput = cleanOutput.replace("\\r", "")

    #print(cleanOutput)

    myList = cleanOutput.split('\\n')

    for line in myList:
        #print(line)
        if not line == "":
            valOne += int(line)

    #print(valOne)
    #print(sum(myList))

    #print(cleanOut)
    print("Stream "+str(streamNum)+": "+str(f'{valOne:,}')+" Bytes")

    return(valOne)