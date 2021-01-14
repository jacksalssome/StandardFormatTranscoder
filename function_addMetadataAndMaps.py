from prettytable import PrettyTable
from compareSizes import compareSizes


def addMetadataAndMaps(filename, metadataTable, totalNumOfStreams, currentOS, engAudioNoSubs):

    # print("Started main2")

    mapThisStream = []  # Don't add streams non eng/jpn streams
    outputStreamNum = 0  # apply the metadata to the final stream number for ffmpeg will forget when it maps the streams "Stream #0:12 -> #0:3 (copy)"

    metadataOptions = ""

    defaultSubSelected = False  # Becomes True when a Default Sub stream is selected
    defaultAudioSelected = False  # Becomes True when a Default Audio stream is selected
    firstAudioStreamLang = ""
    firstAudioStreamTitle = ""
    firstAudioFound = False  # For adding sub/signs if its the only sub track
    firstAudioStreamNum = -1
    signSongsStream = []
    listOfEngSubs = []
    titleOfEngSubs = []
    langOfEngSubs = []
    mapThisStreamIfNoSubsFound = []
    definiteDefaultSubFound = False
    japAudioFound = False

    foreignWarning = False

    for lineNum in range(0, totalNumOfStreams):
        addAudioInfo = True
        titleLang = "\""

        # Populate temp variables with data from prettytable
        metaTitle = (metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["title"]).strip()).lower()  # .lower() for case insensitive
        metaLang = (metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["language"]).strip()).lower()
        metaCodecType = (metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["codec_type"]).strip()).lower()
        metaChannels = metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["channels"]).strip()

        # Handles both audio and subtitles

        if metaTitle.find("signs") != -1 or metaTitle.find("songs") != -1:
            titleLang += "Signs / Songs"
            metaLang = "und"  # We'll und signs/song
        elif metaLang == "jpn":
            titleLang += "Japanese"
        elif metaLang == "eng":
            titleLang += "English"
        else:  # no eng/jpn found though language tags, check titles:
            if metaTitle.find("english") != -1 or metaTitle.find("inglês") != -1:
                titleLang += "English"
                metaLang = "eng"
                print("Found Title Via Backup way")
            elif metaTitle.find("japanese") != -1 or metaTitle.find("Japonês") != -1:
                titleLang += "Japanese"
                metaLang = "jpn"
                print("Found Title Via Backup way")
            else:  # No eng or jpn found:
                addAudioInfo = False
                aLanguageWasFound = False

        # Closed Captioning
        if metaTitle.find("[cc]") != -1 or metaTitle.find("(cc)") != -1:
            titleLang += " (CC)"

        if metaTitle.find("full subs") != -1 or metaTitle.find("full subtitle") != -1 and defaultSubSelected is False:  # if the sub's title is "full subs", then we found your default
            metadataOptions += " -disposition:" + str(outputStreamNum) + " default"
            titleLang = "\"English, Full Subtitles"  # We'll rename for this
            definiteDefaultSubFound = True

        if addAudioInfo is True:
            if metaChannels == "2":
                titleLang += " (2.0)"
            elif metaChannels == "3":  # LOL if someone uses this
                titleLang += " (2.1)"
            elif metaChannels == "4":
                titleLang += " (4.0)"
            elif metaChannels == "5":
                titleLang += " (5.0)"
            elif metaChannels == "6":
                titleLang += " (5.1)"
            elif metaChannels == "7":
                titleLang += " (7.0)"
            elif metaChannels == "8":
                titleLang += " (7.1)"

        titleLang += "\""  # zip up titleLang

        # ---- DEFAULT STREAMS ----

        if defaultAudioSelected is False and metaCodecType == "audio" and metaLang == "jpn":  # Check if first Jap Audio and set as default
            defaultAudioSelected = True
            japAudioFound = True
            metadataOptions += " -disposition:" + str(outputStreamNum) + " default"
        elif metaCodecType == "audio" and defaultAudioSelected is False:  # Make all other audio stream's not default
            metadataOptions += " -disposition:" + str(outputStreamNum) + " 0"

        if defaultSubSelected is False and metaCodecType == "subtitle" and metaLang == "eng":  # Check if first Eng Sub and set as default
            defaultAudioSelected = True
            listOfEngSubs.append(lineNum)
            titleOfEngSubs.append(titleLang)
            langOfEngSubs.append(metaLang)
            outputStreamNum += 1
        elif titleLang == "\"Signs / Songs\"":
            signSongsStream.append(outputStreamNum)
            outputStreamNum += 1
        elif defaultSubSelected is False and metaCodecType == "subtitle" and metaLang == "und":
            mapThisStreamIfNoSubsFound.append(lineNum)

        # ---- ADDING METADATA ----

        if metaCodecType == "video":  # Add the video stream
            mapThisStream.append(lineNum)
            outputStreamNum += 1  # A stream has been definitely added to the output

        if metaLang != "und":  # Don't title non eng/jpn (all stream com in as und and were renamed earlier)
            if metaCodecType != "video":  # Don't title video streams or
                if metaCodecType == "subtitle" and metaLang != "eng" or metaCodecType == "audio":  # Don't add english subs, they will come later
                    metadataOptions += (" -metadata:s:" + str(outputStreamNum) + " title=" + titleLang)
                    metadataOptions += (" -metadata:s:" + str(outputStreamNum) + " language=" + metaLang)
                    mapThisStream.append(lineNum)
                    outputStreamNum += 1
        if metaCodecType == "audio" and firstAudioFound is False and metaLang == "und":  # Incase there is no jap audio
            firstAudioFound = True
            firstAudioStreamLang = metaTitle
            firstAudioStreamNum = lineNum
        elif metaCodecType == "audio" and firstAudioStreamLang == "und" and metaLang == "eng":  # Rather have eng audio then und
            firstAudioFound = True
            firstAudioStreamTitle = metaTitle
            firstAudioStreamLang = metaLang
            firstAudioStreamNum = lineNum

    # ---- END FOR LOOP ----

    if japAudioFound is False and firstAudioStreamLang == "eng" and engAudioNoSubs is True:
        definiteDefaultSubFound = True
        # -- ADD ENGLISH SUBS --
    elif japAudioFound is True and len(listOfEngSubs) >= 1:
        for num in range(0, len(listOfEngSubs)):
            metadataOptions += (" -metadata:s:" + str(listOfEngSubs[num]) + " title=" + str(titleOfEngSubs[num]))
            metadataOptions += (" -metadata:s:" + str(listOfEngSubs[num]) + " language=" + str(langOfEngSubs[num]))
            mapThisStream.append(listOfEngSubs[num])

    if japAudioFound is False and firstAudioStreamNum != -1:  # No jpn audio was found, so add the first audio stream, or the first eng audio
        mapThisStream.append(firstAudioStreamNum)
        metadataOptions += " -disposition:" + str(outputStreamNum) + " default"
        metadataOptions += (" -metadata:s:" + str(outputStreamNum) + " language=" + firstAudioStreamLang)
        metadataOptions += (" -metadata:s:" + str(outputStreamNum) + " title=" + firstAudioStreamTitle)

    if len(signSongsStream) != 0:  # Add a sign/song Tracks, make it default if theres no eng/jpn one found
        for item in signSongsStream:
            mapThisStream.append(item)
            metadataOptions += (" -metadata:s:" + str(item) + " title=\"Signs/Songs\"" )
            if defaultSubSelected is False:  # Only add the first sign/songs
                metadataOptions += " -disposition:" + str(item) + " default"
                defaultSubSelected = True

    # ---- Choose Default sub if more then one english sub ----
    # Also handles detection of foreign audio without an english sub
    if definiteDefaultSubFound is False:
        if len(listOfEngSubs) == 0 and firstAudioStreamLang == "und":
            # No English Subs to go with a foreign audio stream
            foreignWarning = True
        elif len(listOfEngSubs) == 1:  # set default if theres only one eng sub
            defaultSubSelected = True
            metadataOptions += " -disposition:" + str(listOfEngSubs[0]) + " default"
        elif len(listOfEngSubs) >= 2:

            biggestStreamSize = 0
            biggestStreamNum = 0
            secondBiggestStreamSize = 0
            secondBiggestStreamNum = 0
            selBiggestStream = False

            for num in range(0, len(listOfEngSubs)):  # Start iterating from the first sub

                streamSize = compareSizes(num, filename, currentOS)

                if len(listOfEngSubs) == 2:  # Just select the biggest if theres only 2 subs
                    selBiggestStream = True
                    if streamSize > biggestStreamSize:
                        biggestStreamSize = streamSize
                        biggestStreamNum = outputStreamNum

                elif len(listOfEngSubs) >= 3:  # select the second biggest if theres more then 2 subs
                    if streamSize > biggestStreamSize:  # If current stream is biggest
                        biggestStreamSize = streamSize
                    elif streamSize > secondBiggestStreamSize:  # If the current stream is not the biggest, but bigger the the second biggest
                        secondBiggestStreamSize = streamSize
                        secondBiggestStreamNum = outputStreamNum

            if selBiggestStream == True:
                metadataOptions += " -disposition:" + str(biggestStreamNum) + " default"
            else:
                metadataOptions += " -disposition:" + str(secondBiggestStreamNum) + " default"
            defaultSubSelected = True

    outputMaps = ""
    for item in mapThisStream:
        outputMaps += " -map 0:" + str(item)  # -map 0:3
        # Could add prettyTables here and only print the index with item (number)
        # E.g. outputTable += (metadataTable.get_string(start=item, end=item + 1, fields=['Index', 'title', 'language', 'codec_type', 'channels']).strip())

    metadataAndMaps = metadataOptions + outputMaps

    # Print(outputTable.get_string())

    return metadataAndMaps, foreignWarning
