import os
from prettytable import PrettyTable
import ffmpeg
import json


def getAndSaveMetadata(filename):

    # Overview: Call ffmpeg for an output, save to file, read that file line by line in to a PrettyTable for processing. Plus the number of streams.

    #ffprobeOut = json.dumps(ffmpeg.probe(filename), indent=4)
    #print(json.dumps(ffmpeg.probe(filename), indent=4))

    os.system("cmd /c ffprobe -v error -show_streams \"" + filename + "\" > \"Metadata\\" + filename + "(All).txt\" 2>&1")

    txtfile = open("Metadata\\" + filename + "(all).txt", encoding="utf8")

    metadataTable = PrettyTable(['Index', 'title', 'language', 'codec_type', 'channels'])

    metadataTableIndex = ""
    metadataTableTitle = ""
    metadataTableLang = ""
    metadataTableCodecType = ""
    metadataTableChannels = ""
    totalNumOfStreams = 0

    for line in txtfile:
        if line.find("index=") != -1:
            if str(line[6:8].replace('\n', '')) != "0":
                metadataTable.add_row([metadataTableIndex, metadataTableTitle, metadataTableLang, metadataTableCodecType, metadataTableChannels])
                # print(metadataTable.get_string(start=rowNum, end=rowNum + 1, fields=["Index"]))
                #rowNum += 1
                metadataTableIndex = ""
                metadataTableTitle = ""
                metadataTableLang = ""
                metadataTableCodecType = ""
                metadataTableChannels = ""
                totalNumOfStreams += 1
            metadataTableIndex = line[6:8].replace('\n', '')

        elif line.find("TAG:title=") != -1:
            metadataTableTitle = line[10:line.find("/n")]
        elif line.find("TAG:language") != -1:
            metadataTableLang = line[13:line.find("/n")]
        elif line.find("codec_type=") != -1:
            metadataTableCodecType = line[11:line.find("/n")]
        elif line.find("channels=") != -1:
            metadataTableChannels = line[9:line.find("/n")]
        #elif line.find("codec_name=") != -1:
        #    currentLine = currentLine + line + " "
        #    metadataTableCodecName = "codec_name=" + str(lineNum)

    metadataTable.add_row([metadataTableIndex, metadataTableTitle, metadataTableLang, metadataTableCodecType, metadataTableChannels])  # add last row
    totalNumOfStreams += 1  # last row

    #metadataTable.border = False
    #metadataTable.header = False
    #print(metadataTable.get_string(start=12, end=12 + 1, fields=["Index"]).strip())
    #print(metadataTable.get_string(start=12, end=12 + 1, fields=["language"]).strip())
    #print(metadataTable.get_string())
    metadataTable.border = False
    metadataTable.header = False

    #print(totalNumOfStreams, "test")

    return(metadataTable, totalNumOfStreams)
