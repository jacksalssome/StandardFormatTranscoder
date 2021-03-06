from prettytable import PrettyTable
from colorama import Fore
from function_findBestEngSubStream import findBestEngSubStream
from function_getNumOfAudioAndSubs import *


def addMetadataAndMaps(filename, metadataTable, totalNumOfStreams, currentOS, ifEngAudioThenNoSubs, infoMessages):

    outputTable = PrettyTable(["Index", "Title", "Language", "CodecType", "CodecName"])
    outputTable.border, outputTable.header, defaultEngSubFound = False, False, False
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

        if "signs" in metaTitle or "songs" in metaTitle:
            streamTitle += "Signs / Songs"
            metaLang = "SignsSongs"  # We'll und signs/song
        elif metaLang == "jpn":
            streamTitle += "Japanese"
        elif metaLang == "eng":
            streamTitle += "English"
        else:  # no eng/jpn found though language tags, check titles:
            if "english" in metaTitle or "inglês" in metaTitle:
                streamTitle += "English"
                metaLang = "eng"
                #print(Fore.CYAN + "Found Sub/Audio Title Via Backup way" + Fore.RESET)
                infoMessages += 1
            elif "japanese" in metaTitle or "japonês" in metaTitle:
                streamTitle += "Japanese"
                metaLang = "jpn"
                #print(Fore.CYAN + "Found Sub/Audio Title Via Backup way" + Fore.RESET)
                infoMessages += 1
            else:  # No eng or jpn found:
                metaLang = "und"
                addAudioInfo = False

        # Closed Captioning
        if metaTitle.find("[cc]") != -1 or metaTitle.find("(cc)") != -1:
            streamTitle += " (CC)"

        if metaLang == "eng":
            for item in ["dialogue", "full subs", "full subtitle", "[full]", "(full)", "modified"]:  # if sub's title is one of these, then make it default
                if item in metaTitle:
                    addDefault = True
                    streamTitle = "\"English, Full Subtitles"  # We'll rename for this
                    defaultEngSubFound = True
                    break
            tempList = ["commentary", "comment"]
            for item in tempList:
                if item in metaTitle:
                    streamTitle = "\"Commentary"
                    break

        if addAudioInfo is True:
            if metaChannels == "2":
                streamTitle += " (2.0)"
            elif metaChannels == "3":
                streamTitle += " (2.1)"
            elif metaChannels == "4":
                streamTitle += " (4.0)"
            elif metaChannels == "5":  # LOL if someone uses these odd ones
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

        defaultStreams.append(addDefault)  # IsDefault is separate because i couldn't find a way to change a single cell in the table.
        #                       Index               Title           Language            Codec
        outputTable.add_row([outputTableIndex, outputTableTitle, outputTableLang, outputTableCodec, metaCodecName])

    # ---- END FOR LOOP ----

    jpnAudioFound, engSubFound, engAudioFound = False, False, False
    listOfEngSubs = []
    tempNum = 0
    for i in outputTable:
        if findEngSub(outputTable, tempNum) is True and defaultStreams[tempNum] is True:
            engSubFound = True
            break
        elif findEngSub(outputTable, tempNum) is True:
            if defaultEngSubFound is False:  # check if a default eng sub has been set
                engSubFound = True
            listOfEngSubs.append(tempNum)
        elif findJpnAudio(outputTable, tempNum) is True:
            defaultStreams[tempNum] = "True"
            jpnAudioFound = True
        elif findEngAudio(outputTable, tempNum) is True:
            engAudioFound = True
        tempNum += 1

    if jpnAudioFound is True or engAudioFound is False:
        if len(listOfEngSubs) == 1:
            defaultStreams[listOfEngSubs[0]] = "True"
        elif len(listOfEngSubs) >= 2:
            row = findBestEngSubStream(listOfEngSubs, filename, currentOS)
            defaultStreams[row] = "True"

    outputTable.add_column('IsDefault', defaultStreams)  # Add IsDefault to Table

    tempNumber = 0
    outCodecType, outCodecName, outLang = [], [], []

    for i in outputTable:
        # Cant work directly on the prettyTable, or it will delete the rows your working on, even it you tell it to delete from another table
        # So i cheat and convert the columns i need to lists, why did i make a table in the first place?
        # Because i didn't want to keep 6 lists in sync.
        outLang.append(str(outputTable.get_string(start=tempNumber, end=tempNumber + 1, fields=["Language"]).strip()))
        outCodecType.append(str(outputTable.get_string(start=tempNumber, end=tempNumber + 1, fields=["CodecType"]).strip()))
        outCodecName.append(str(outputTable.get_string(start=tempNumber, end=tempNumber + 1, fields=["CodecName"]).strip()))
        tempNumber += 1

    tempNum, addedSubs, deletedRows = 0, 0, 0

    for item in range(0, len(outLang)):
        # Things We Want To Remove:
        if jpnAudioFound is True:
            if outCodecType[tempNum] == "subtitle" and (outLang[tempNum] == "und" or outLang[tempNum] == "jpn"):
                if not outLang[tempNum] == "SignsSongs":
                    if engSubFound is False and addedSubs == 0:
                        addedSubs += 1
                    else:
                        outputTable.del_row(tempNum - deletedRows)  # Delete the current table row
                        deletedRows += 1  # So we can track how many rows are missing (This took a day to figure out)
            elif outCodecType[tempNum] == "audio" and outLang[tempNum] == "und":
                outputTable.del_row(tempNum - deletedRows)
                deletedRows += 1
        elif engAudioFound is True:  # Theres no JPN AUDIO if the program got to here
            if outCodecType[tempNum] == "audio" and outLang[tempNum] == "und":
                outputTable.del_row(tempNum - deletedRows)
                deletedRows += 1
            elif outCodecType[tempNum] == "subtitle" and ifEngAudioThenNoSubs is True:  # Remove all subs if ifEngAudioThenNoSubs is True
                outputTable.del_row(tempNum - deletedRows)
                deletedRows += 1
        elif engAudioFound is False:  # Theres no JPN AUDIO if the program got to here
            if engSubFound is True:  # If theres not eng audio and no eng subs, then keep all audio and subs
                if outCodecType[tempNum] == "subtitle" and outLang[tempNum] == "und":
                    outputTable.del_row(tempNum - deletedRows)
                    deletedRows += 1
        if outCodecType[tempNum] in ("attachment", "image", "data", "text"):
            outputTable.del_row(tempNum - deletedRows)
            deletedRows += 1
        if outCodecName[tempNum] == "mjpeg":
            outputTable.del_row(tempNum - deletedRows)
            deletedRows += 1
        tempNum += 1
    # END Loop

    tempNum = 0
    outputDisposition = ""
    for i in outputTable:  # Convert to output streams, e.g. -map 0:0, -map 0:1, -map 0:2
        isItDefault = outputTable.get_string(start=tempNum, end=tempNum + 1, fields=["IsDefault"]).split()
        if "True" in isItDefault:
            outputDisposition += " -disposition:" + str(tempNum).replace("[\'", "").replace("\']", "") + " default"
        elif "False" in isItDefault:
            outputDisposition += " -disposition:" + str(tempNum).replace("[\'", "").replace("\']", "") + " 0"
        tempNum += 1

    tempNum = 0
    outputMetadata = ""
    for i in outputTable:  # Convert to output streams, e.g. -map 0:0, -map 0:1, -map 0:2
        title = outputTable.get_string(start=tempNum, end=tempNum + 1, fields=["Title"]).split()
        language = outputTable.get_string(start=tempNum, end=tempNum + 1, fields=["Language"]).split()
        outputMetadata += " -metadata:s:" + str(tempNum) + " title=" + str(title).replace("[\'", "").replace("\']", "").replace("\', \'", " ")
        outputMetadata += " -metadata:s:" + str(tempNum) + " language=" + str(language).replace("[\'", "").replace("\']", "").replace("\', \'", " ")
        tempNum += 1

    outputMaps = ""
    tempNum = 0
    for i in outputTable:  # Convert to output streams, e.g. -map 0:0, -map 0:1, -map 0:2
        mapNum = outputTable.get_string(start=tempNum, end=tempNum + 1, fields=["Index"]).split()
        outputMaps += " -map 0:" + str(mapNum).replace("[\'", "").replace("\']", "")  # -map 0:3
        tempNum += 1

    metadataAndMaps = outputMetadata + outputDisposition + outputMaps

    #print(outputDisposition)

    #outputTable.border = True
    #outputTable.header = True
    #print(outputTable.get_string())

    return metadataAndMaps, infoMessages
