from prettytable import PrettyTable
from colorama import Fore
from function_findBestEngSubStream import findBestEngSubStream
from function_getNumOfAudioAndSubs import *


def addMetadataAndMaps(filename, metadataTable, totalNumOfStreams, currentOS, engAudioNoSubs, infos):

    outputTable = PrettyTable(["Index", "Title", "Language", "CodecType", "CodecName"])
    outputTable.border = False
    outputTable.header = False
    defaultStreams = []

    # Adding titles and making output prettyTable
    for lineNum in range(0, totalNumOfStreams):
        addAudioInfo = True
        streamTitle = "\""
        addDefault = False
        # Populate temp variables with data from prettyTable
        metaTitle = (metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["title"]).strip()).lower()  # .lower() for case insensitive
        metaLang = (metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["language"]).strip()).lower()
        metaCodecType = (metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["codec_type"]).strip()).lower()
        metaChannels = metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["channels"]).strip()
        metaCodecName = (metadataTable.get_string(start=lineNum, end=lineNum + 1, fields=["codec_name"]).strip()).lower()

        # Handles both audio and subtitles

        if metaTitle.find("signs") != -1 or metaTitle.find("songs") != -1:
            streamTitle += "Signs / Songs"
            metaLang = "und"  # We'll und signs/song
        elif metaLang == "jpn":
            streamTitle += "Japanese"
        elif metaLang == "eng":
            streamTitle += "English"
        else:  # no eng/jpn found though language tags, check titles:
            if metaTitle.find("english") != -1 or metaTitle.find("inglês") != -1:
                streamTitle += "English"
                metaLang = "eng"
                print(Fore.CYAN + "Found Title Via Backup way" + Fore.RESET)
                infos += 1
            elif metaTitle.find("japanese") != -1 or metaTitle.find("Japonês") != -1:
                streamTitle += "Japanese"
                metaLang = "jpn"
                print(Fore.CYAN + "Found Title Via Backup way" + Fore.RESET)
                infos += 1
            else:  # No eng or jpn found:
                metaLang = "und"
                addAudioInfo = False

        # Closed Captioning
        if metaTitle.find("[cc]") != -1 or metaTitle.find("(cc)") != -1:
            streamTitle += " (CC)"

        if metaLang == "eng":
            for item in ["dialogue", "full subs", "full subtitle", "[full]", "(full)", "modified"]:  # if sub's title is one of these, then make it default
                if metaTitle.find(item) != -1:
                    addDefault = True
                    streamTitle = "\"English, Full Subtitles"  # We'll rename for this
                    break

        if addAudioInfo is True:
            if metaChannels == "2":
                streamTitle += " (2.0)"
            elif metaChannels == "3":  # LOL if someone uses this
                streamTitle += " (2.1)"
            elif metaChannels == "4":
                streamTitle += " (4.0)"
            elif metaChannels == "5":
                streamTitle += " (5.0)"
            elif metaChannels == "6":
                streamTitle += " (5.1)"
            elif metaChannels == "7":
                streamTitle += " (7.0)"
            elif metaChannels == "8":
                streamTitle += " (7.1)"

        streamTitle += "\""

        if metaCodecType == "video":
            metaLang = "und"
            streamTitle = "\"\""

        outputTableIndex = str(lineNum)
        outputTableTitle = str(streamTitle)
        outputTableLang = str(metaLang)
        outputTableCodec = str(metaCodecType)

        defaultStreams.append(addDefault)
        #                       Index               Title           Language            Codec
        outputTable.add_row([outputTableIndex, outputTableTitle, outputTableLang, outputTableCodec, metaCodecName])

    # ---- END FOR LOOP ----

    jpnAudioFound = False
    engAudioFound = False
    listOfEngSubs = []
    engSubFound = False
    engsub = 0
    tempNum = 0
    for item in outputTable:
        if findEngSub(outputTable, tempNum) is True and defaultStreams[tempNum] is True:
            engSubFound = True
            break
        elif findEngSub(outputTable, tempNum) is True:
            engSubFound = True
            listOfEngSubs.append(tempNum)
        elif findJpnAudio(outputTable, tempNum) is True:
            defaultStreams[tempNum] = True
            jpnAudioFound = True
        elif findEngAudio(outputTable, tempNum) is True:
            engAudioFound = True
        tempNum += 1

    if len(listOfEngSubs) == 1:
        defaultStreams[engsub] = True
    elif len(listOfEngSubs) >= 2:
        row = findBestEngSubStream(listOfEngSubs, filename, currentOS)
        defaultStreams[row] = True

    tempNumber = 0
    outLang = []
    outCodecType = []
    outCodecName = []
    for item in outputTable:  # Cant work directly on the prettyTable, or it will delete the rows your working on, even it you tell it to delete from another table
        outLang.append(str(outputTable.get_string(start=tempNumber, end=tempNumber + 1, fields=["Language"]).strip()))
        outCodecType.append(str(outputTable.get_string(start=tempNumber, end=tempNumber + 1, fields=["CodecType"]).strip()))
        outCodecName.append(str(outputTable.get_string(start=tempNumber, end=tempNumber + 1, fields=["CodecName"]).strip()))
        tempNumber += 1

    tempNum = 0
    deletedRows = 0
    for item in range(0, len(outLang)):

        # Things We Want To Remove:
        if jpnAudioFound is True:
            if outCodecType[tempNum] == "subtitle" and outLang[tempNum] == "und":
                outputTable.del_row(tempNum - deletedRows)
                del defaultStreams[tempNum - deletedRows]
                deletedRows += 1
            elif outCodecType[tempNum] == "audio" and outLang[tempNum] == "und":
                outputTable.del_row(tempNum - deletedRows)
                del defaultStreams[tempNum - deletedRows]
                deletedRows += 1

        elif engAudioFound is True:  # Theres no JPN AUDIO if the program got to here
            if outCodecType[tempNum] == "audio" and outLang[tempNum] == "und":
                outputTable.del_row(tempNum - deletedRows)
                del defaultStreams[tempNum - deletedRows]
                deletedRows += 1
            elif outCodecType[tempNum] == "subtitle":  # Remove all subs since its english audio
                outputTable.del_row(tempNum - deletedRows)
                del defaultStreams[tempNum - deletedRows]
                deletedRows += 1

        elif engAudioFound is False:  # Theres no JPN AUDIO if the program got to here
            if engSubFound is True:  # If theres not eng audio and no eng subs, then keep all audio and subs
                if outCodecType[tempNum] == "subtitle" and outLang[tempNum] == "und":
                    outputTable.del_row(tempNum - deletedRows)
                    del defaultStreams[tempNum - deletedRows]
                    deletedRows += 1
        if outCodecType[tempNum] == "attachment":
            outputTable.del_row(tempNum - deletedRows)
            del defaultStreams[tempNum - deletedRows]
            deletedRows += 1
        if outCodecName[tempNum] == "mjpeg":
            outputTable.del_row(tempNum - deletedRows)
            del defaultStreams[tempNum - deletedRows]
            deletedRows += 1

        tempNum += 1

    # END Loop
    outputTable.add_column('IsDefault', defaultStreams)

    tempNum = 0
    outputDisposition = ""
    for row in defaultStreams:  # Convert to output streams, e.g. -map 0:0, -map 0:1, -map 0:2
        disposition = outputTable.get_string(start=tempNum, end=tempNum + 1, fields=["Index"]).split()
        if row is True:
            outputDisposition += " -disposition:" + str(disposition).replace("[\'", "").replace("\']", "") + " default"
        elif row is False:
            outputDisposition += " -disposition:" + str(disposition).replace("[\'", "").replace("\']", "") + " 0"
        tempNum += 1

    tempNum = 0
    outputMetadata = ""
    for row in outputTable:  # Convert to output streams, e.g. -map 0:0, -map 0:1, -map 0:2
        title = outputTable.get_string(start=tempNum, end=tempNum + 1, fields=["Title"]).split()
        language = outputTable.get_string(start=tempNum, end=tempNum + 1, fields=["Language"]).split()
        outputMetadata += " -metadata:s:" + str(tempNum) + " title=" + str(title).replace("[\'", "").replace("\']", "").replace("\', \'", " ")
        outputMetadata += " -metadata:s:" + str(tempNum) + " language=" + str(language).replace("[\'", "").replace("\']", "").replace("\', \'", " ")
        tempNum += 1

    outputMaps = ""
    tempNum = 0
    for row in outputTable:  # Convert to output streams, e.g. -map 0:0, -map 0:1, -map 0:2
        mapNum = outputTable.get_string(start=tempNum, end=tempNum + 1, fields=["Index"]).split()
        outputMaps += " -map 0:" + str(mapNum).replace("[\'", "").replace("\']", "")  # -map 0:3
        tempNum += 1

    metadataAndMaps = outputMetadata + outputDisposition + outputMaps

    # Print(outputTable.get_string())
    foreignWarning = False
    return metadataAndMaps, foreignWarning, infos
