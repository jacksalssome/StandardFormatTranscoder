from prettytable import PrettyTable
from colorama import Fore
import subprocess


def getAndSaveMetadata(filename, filenameAndDirectory, currentOS):

    # Overview: Call ffmpeg for an output, save to file, read that file line by line in to a PrettyTable for processing. Plus the number of streams.

    metadataTable = PrettyTable(['Index', 'title', 'language', 'codec_type', 'channels', 'codec_name'])

    metadataTableIndex = ""
    metadataTableTitle = ""
    metadataTableLang = ""
    metadataTableCodecType = ""
    metadataTableChannels = ""
    metadataTableCodecName = ""
    totalNumOfStreams = 0
    firstIteration = False
    ffmpegDumps = ""

    try:
        if currentOS == "Linux":
            ffmpegDumps = str(subprocess.check_output("ffprobe -v quiet -print_format json -show_format -show_streams \"" + filenameAndDirectory + "\"", shell=False))
        if currentOS == "Windows":
            ffmpegDumps = str(subprocess.check_output("cmd /c ffprobe -v quiet -print_format json -show_format -show_streams \"" + filenameAndDirectory + "\"", shell=False))
    except:
        print(Fore.RED + "Theres a problem with the input file: \"" + Fore.RESET + filename + Fore.RED + "\"" + Fore.RESET)
        print(Fore.RED + "Possible corruption, incomplete file or permissions problem" + Fore.RESET)
        return None

    for line in str(ffmpegDumps).split("\\r\\n"):  # Check it out, i wrote my own JSON interpreter, why do i use JSON? Because this originally used the ffmpeg-python module.

        #print(str(line))

        lenAdjust = 2  # Usually there will be a , at the end of the line, so well set the variable and check if its right.
        if line[len(line) - 1] == "\"":
            lenAdjust = 1
        elif line[len(line) - 2] != "\"" and line[len(line) - 1] == ",":
            lenAdjust = 1

        if line.find("\"index\":") != -1:

            if firstIteration is True:
                metadataTable.add_row([metadataTableIndex, metadataTableTitle, metadataTableLang, metadataTableCodecType, metadataTableChannels, metadataTableCodecName])
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
        elif line.find("codec_name") != -1:
            metadataTableCodecName = line[27:len(line) - lenAdjust]

    metadataTable.add_row([metadataTableIndex, metadataTableTitle, metadataTableLang, metadataTableCodecType, metadataTableChannels, metadataTableCodecName])  # add last row
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
