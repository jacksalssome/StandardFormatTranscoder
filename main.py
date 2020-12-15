import os
from pathlib import Path
import shutil

directory = os.path.dirname(os.path.realpath(__file__))

#print(directory)
#print(os.listdir(directory))

print("Transcode Starting")
Path("MKVoutput/").mkdir(parents=True, exist_ok=True)
Path("Metadata/").mkdir(parents=True, exist_ok=True)

iterations = 0
for filename in os.listdir(directory):
    if filename.endswith(".mkv"): # Find Any MKV files
        iterations = iterations + 1 # Log how many files we change
        # -- Get Metadata from source file and tidy them up --
        os.system("cmd /c ffmpeg -i \""+filename+"\" > \"Metadata\\"+filename+".txt\" 2>&1")
        os.system("cmd /c findstr /I /C:\"Stream #\" \"Metadata\\"+filename+".txt\" > \"Metadata\\"+filename+"(step1).txt\" 2>&1")
        # Following removes attachment streams
        os.system("cmd /c findstr /I /V \"Attachment Guessed\" \"Metadata\\"+filename+"(step1).txt\" > \"Metadata\\" + filename + "(stripped).txt\" 2>&1")

        os.system("cmd /c ffprobe -v error -show_streams \"" + filename + "\" > \"Metadata\\" + filename + "(All).txt\" 2>&1")
        os.system("cmd /c findstr /I \"TAG:title index=\" \"Metadata\\" + filename + "(All).txt\" > \"Metadata\\" + filename + "(stream_titles).txt\" 2>&1")

        # -- Open Metadate file for processing --

        txtfile = open("Metadata\\"+filename+"(stripped).txt")  # Most metadatea language, stereo,5.1, etc
        txtfile2 = open("Metadata\\" + filename + "(stream_titles).txt")  # Just the titles

        skipStreamNum = ""
        metadataOptions = ""
        streamNumber = -1

        # -- First check for "Signs / Songs" --

        for line2 in txtfile2:

            if line2.find("index=") != -1:
                if len(line2) == 8:  # Double didgit Check
                    #print(line2[6])
                    streamNumber = line2[6]
                else:
                    #print(line2[6:8])
                    streamNumber = line2[6:8]

            if line2.find("Signs / Songs") != -1 or line2.find("Signs / Songs") != -1:  # Subtitles
                skipStreamNum = skipStreamNum + "'" +str(streamNumber) + "'"
                #print("Skip stream: "+skipStreamNum)
                titleLang = "\"Signs / Songs\""
                metadataOptions = metadataOptions + (" -metadata:s:" + streamNumber + " title=" + titleLang)

        txtfile2.close()

        # Check language tags and titles for a language, if one
        # is found then add on the audio type eg. English (stereo)

        for line in txtfile:
            titleLang = "\""
            addAudioInfo = False
            aLanguageWasFound = False

            if not skipStreamNum.find("'" + str(line[14]) + "'") != -1:
                if line.find("(eng)") != -1:
                    titleLang = titleLang+"English"
                    addAudioInfo = True
                    aLanguageWasFound = True
                elif line.find("(jpn)") != -1:
                    titleLang = titleLang+"Japanese"
                    addAudioInfo = True
                    aLanguageWasFound = True

                if aLanguageWasFound == False:
                    skipToNextLine = False
                    txtfile2 = open("Metadata\\" + filename + "(stream_titles).txt")
                    for line2 in txtfile2:
                        if skipToNextLine == True:
                            skipToNextLine = False
                            if line2.find("English") != -1:
                                titleLang = titleLang + "English"
                                addAudioInfo = True
                                #print("Found Title Via Backup way")
                            elif line2.find("Japanese") != -1:
                                titleLang = titleLang + "Japanese"
                                addAudioInfo = True
                                #print("Found Title Via Backup way")
                            break
                        if line2.find("index=" + str(line[14])) != -1:
                            if (len(line2) == 8 and str(line[15]) == ":") or (len(line2) == 9 and str(line[15]) != ":"):
                                #print(line2)
                                skipToNextLine = True
                    txtfile2.close()

                if addAudioInfo == True:
                    if line.find(", stereo,") != -1:
                        titleLang = titleLang+" (2.0)"
                    elif line.find(", 5.1,") != -1:
                        titleLang = titleLang + " (5.1)"

                titleLang = titleLang + "\""
                metadataOptions = metadataOptions + (" -metadata:s:" + line[14] + " title=" + titleLang)
                #print(metadataOptions)

                # -- remove mjpeg video streams --

        txtfile.close()

        txtfile = open("Metadata\\"+filename+"(stripped).txt") # map only v:a:s streams, not attachments
        numberOfMaps = ""
        lineNum = 0
        for line3 in txtfile:
            if line3.find("mjpeg") == -1:
                numberOfMaps = numberOfMaps+" -map 0:"+str(lineNum)
            lineNum = lineNum+1

        txtfile.close()

        #print(numberOfMaps)

        #print("cmd /c ffmpeg -v error -n -i \""+filename+"\" -map_metadata -1"+metadataOptions+numberOfMaps+" -c copy -copy_unknown \"MKVoutput\\"+filename+"\"")

        os.system("cmd /c ffmpeg -v error -n -i \""+filename+"\" -map_chapters 0"+metadataOptions+numberOfMaps+" -metadata title="" -c copy -copy_unknown \"MKVoutput\\"+filename+"\"")


        #print(os.path.join(directory, filename))

        print("Done: " + filename)

# Remove metadata directory

#try:
#    shutil.rmtree("Metadata")
#except OSError as e:
#    print("Error: %s : %s" % ("Metadata", e.strerror))

print("Finished", iterations, "files")
input("Press ENTER to exit")

