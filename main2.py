from prettytable import PrettyTable

def main2(filename, metadataTable, totalNumOfStreams):

    # Overview:

    # Get the preety table and read each row, create variables for each colum. Check variable for relevent info.
    # First for loop handels meatdata entry, sets defaults streams
    # Second for loop handles mapping so we don't copy over wanted streams and handels minium amount or streams.


    #print("Started main2")


    mapThisStream = ""  # Don't add streams non eng/jpn streams
    outputStreamNum = 0  # apply the metadata to the final stream number for ffmpeg will forget when it maps the streams "Stream #0:12 -> #0:3 (copy)"

    # Check language tags and titles for a language, if one
    # is found then add on the audio type eg. English (stereo)
    defaultSubSelected = False  # Becomes True when a Default Sub stream is selected
    defaultAudioSelected = False  # Becomes True when a Default Audio stream is selected

    numOfAudioStreams = 0  # Make sure theres at
    firstAudioStreamNum = -1  # lease one Audio Track
    signSongsSubStream = -1
    firstAudioStreamMap = ""  # For adding sub/signs if its the only sub track
    lineNum = 0
    metadataOptions = ""

    for line in range(0, totalNumOfStreams):
        titleLang = "\""  # So i don't have to escape so many times (Theres only one titleLand per loop)
        addAudioInfo = False
        aLanguageWasFound = False
        thisStreamLanguage = "und"

        # Populate temp variables with data from table
        metaTitle = metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["title"]).strip()
        metaLang = metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["language"]).strip()
        metaCodecType = metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["codec_type"]).strip()
        metaChannels = metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["channels"]).strip()

        #print(str(lineNum)+": "+metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["language"]).strip())

        # Handles Audio and subtitles

        if metaTitle.find("Signs") != -1 or metaTitle.find("Songs") != -1:  # Looking for song/signs
            metadataOptions = (" -metadata:s:" + str(outputStreamNum) + "\" title=Signs / Songs\"")
            signSongsSubStream = lineNum
            aLanguageWasFound = True
        elif metaLang == "eng":
            titleLang += "English"
            thisStreamLanguage = "eng"
            addAudioInfo = True
            aLanguageWasFound = True
        elif metaLang == "jpn":
            titleLang += "Japanese"
            thisStreamLanguage = "jpn"
            addAudioInfo = True
            aLanguageWasFound = True

        if aLanguageWasFound is False: # If theres no audio tags then check the streams title
            if metaTitle.find("English") != -1 or metaTitle.find("Inglês") != -1:
                titleLang += "English"
                thisStreamLanguage = "eng"
                addAudioInfo = True
                print("Found Title Via Backup way")

            elif metaTitle.find("Japanese") != -1 or metaTitle.find("Japonês") != -1:
                titleLang += "Japanese"
                thisStreamLanguage = "jpn"
                addAudioInfo = True
                print("Found Title Via Backup way")

        if addAudioInfo is True:
            if metaChannels == "2":
                titleLang += " (2.0)"
            elif metaChannels == "6":
                titleLang += " (5.1)"
            elif metaChannels == "8":
                titleLang += " (7.1)"

        # Default streams

        if defaultAudioSelected is False and metaCodecType == "audio" and thisStreamLanguage == "jpn":  # Check if first Jap Audio and set as default
            defaultAudioSelected = True
            numOfAudioStreams += 1
            metadataOptions += " -disposition:" + str(outputStreamNum) + " default"
        elif metaCodecType == "audio" and defaultAudioSelected is False:  # Stop FFmpeg from making the first audio stream default
            metadataOptions += " -disposition:" + str(outputStreamNum) + " 0"

        if defaultSubSelected is False and metaCodecType == "subtitle" and thisStreamLanguage == "eng" and defaultAudioSelected == True:  # Check if first Eng Audio and set as default
            defaultSubSelected = True
            metadataOptions += " -disposition:" + str(outputStreamNum) + " default"
        elif metaCodecType == "subtitle" and defaultAudioSelected is False:  # Stop FFmpeg from making the first sub stream default
            metadataOptions += " -disposition:" + str(outputStreamNum) + " 0"

        titleLang += "\""  # zip up titleLang

        if thisStreamLanguage != "und":  # Don't title non eng/jpn (all stream com in as und and were renamed earlier)
            if metaCodecType != "video":  # Don't title video streams

                metadataOptions += (" -metadata:s:" + str(outputStreamNum) + " title=" + titleLang)
                metadataOptions += (" -metadata:s:" + str(outputStreamNum) + " language=" + thisStreamLanguage)

                mapThisStream += str(lineNum) + " "
                outputStreamNum += 1

        if metaCodecType.find("video") != -1:  # Add the video stream
            mapThisStream += str(lineNum) + " "
            outputStreamNum += 1

        if metaCodecType == "audio" and firstAudioStreamNum == -1:
            firstAudioStreamMap = str(outputStreamNum) + "( "
            firstAudioStreamNum = lineNum

        #print(metadataOptions)
        #print(outputStreamNum)

        # -- remove mjpeg video streams --

        lineNum += 1

    #txtfile.close()

    if numOfAudioStreams == 0:  # Add an Audio Track if theres no eng/jpn one found
        mapThisStream += firstAudioStreamMap + " "
        metadataOptions += " -disposition:" + str(firstAudioStreamNum) + " default"
        # print(str(firstAudioStreamNum)+"Hi")

    if signSongsSubStream != -1 and defaultSubSelected is False:  # Add an Sub Track if theres no eng/jpn one found
        mapThisStream = mapThisStream + str(signSongsSubStream) + " "
        metadataOptions += " -disposition:" + str(signSongsSubStream) + " default"

    #txtfile = open("Metadata\\"+filename+"(stripped).txt") # map only v:a:s streams, not attachments

    numberOfMaps = ""
    lineNum = 0
    for line2 in range(0, totalNumOfStreams):

        # Populate temp variable with data from table
        metaCodecType = metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["codec_type"]).strip()

        # Don't add mjpeg, attachments, add everything else
        if metaCodecType != "mjpeg" or metaCodecType != "attachment":
            if mapThisStream.find(str(lineNum) + " ") != -1:
                numberOfMaps += " -map 0:"+str(lineNum)

        lineNum += 1

    #txtfile.close()
    #print(mapThisStream)

    metadataAndMaps = metadataOptions+numberOfMaps

    return metadataAndMaps
