import os
from prettytable import PrettyTable
import ffmpeg
import json
import re
from colorama import Fore, Style
import sys


def getAndSaveMetadata(filename, filenameAndDirectory):

    # Overview: Call ffmpeg for an output, save to file, read that file line by line in to a PrettyTable for processing. Plus the number of streams.

    metadataTable = PrettyTable(['Index', 'title', 'language', 'codec_type', 'channels'])

    metadataTableIndex = ""
    metadataTableTitle = ""
    metadataTableLang = ""
    metadataTableCodecType = ""
    metadataTableChannels = ""
    totalNumOfStreams = 0
    firstIteration = False

    try:
        ffmpegDumps = (json.dumps(ffmpeg.probe(filenameAndDirectory), indent=4))
    except:
        print(Fore.RED + "Theres a problem with the input file: " + Style.RESET_ALL + filename)
        print(Fore.RED + "Possible corruption, incomplete file or permissions problem" + Style.RESET_ALL)
        return None

    for line in ffmpegDumps.splitlines():
        #print(line)

        lenAdjust = 2  # Usally there will be a , at the end of the line, so well set the variable and check if its right.
        if line[len(line) - 1] == "\"":
            lenAdjust = 1
        elif line[len(line) - 2] != "\"" and line[len(line) - 1] == ",":
            lenAdjust = 1

        if line.find("\"index\":") != -1:
            #print("Index: " + line[21:len(line) - 1])

            if firstIteration == True:
                metadataTable.add_row([metadataTableIndex, metadataTableTitle, metadataTableLang, metadataTableCodecType, metadataTableChannels])
                # print(metadataTable.get_string(start=rowNum, end=rowNum + 1, fields=["Index"]))
                #rowNum += 1
                metadataTableIndex = ""
                metadataTableTitle = ""
                metadataTableLang = ""
                metadataTableCodecType = ""
                metadataTableChannels = ""
                totalNumOfStreams += 1

            firstIteration = True
            metadataTableIndex = line[21:len(line) - 1]

        elif line.find("\"title\":") != -1:
            metadataTableTitle = line[26:len(line) - lenAdjust]
        elif line.find("\"language\":") != -1:
            metadataTableLang = line[29:len(line) - lenAdjust]
        elif line.find("\"codec_type\":") != -1:
            metadataTableCodecType = line[27:len(line) - lenAdjust]
        elif line.find("\"channels\":") != -1:
            metadataTableChannels = line[24:len(line) - lenAdjust]

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

    #breakpoint()

    return metadataTable, totalNumOfStreams
