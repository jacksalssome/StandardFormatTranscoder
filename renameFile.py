import re


def checkForDups(list): # List duplication checker
    seen = {}
    dupes = []
    for x in list:
        x = x.lower()
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
            seen[x] += 1
    if str(dupes) == "[]":
        print("No Duplicates found")
    else:
        print("Duplicates found in List: " + str(dupes))


def renameFile(filename):

    removeStrings = [  # Remove all strings listed
        "()",
        "[]",
        "{}",
        ".",
        "(Dual Audio_10bit_BD720p_x265)",
        "[AkihitoSubs]",
        "[anime4life.]",
        "[HR]",
        "[JacobSwaggedUp]",
        "[kokus-rips]",
        "[Nep_Blanc]",
        "[ZRIPZ]",
        "[ASW]",
        "[Cleo]",
        "[BD 1080p]",
        "[Opus]",
        "[10Bit]",
        "[x265]",
        "[HEVC]",
        "[BD 1920x1080 x265 10Bit Opus]",
        "(BD1080p AC3 10bit)",
        "Dual Audio",
        "Dual_Audio",
        "[x265_HEVC]",
        "(BD Batch + OVA)",
        "HR-SR",
        "[1080p]",
        "(BD 1280x720)",
        "[Subbed]",
        "(1080p Bluray x265 HEVC 10bit AAC 5.1 Tigole)",
        "[SEV]",
        "1080p",
        "DSNP",
        "WEBrip",
        "x265",
        "D0ct0rLew",
        "[1080p HEVC]",
        "10bit_BD720p_x265)",
        "BD720p",
        "[Pixel]",
        "[BDRip 1080p 10bit HEVC x265 Opus DualAudio(JPN ENG) Subbed Dubbed]",
        "BDRip",
        "Opus",
        "(JPN ENG)",
        "Subbed",
        "Dubbed",
        "[DB]",
        "(Dual Audio_10bit_BD1080p_x265)",
        "[GSK_kun]",
        "[BDRip 1920x1080 x264 FLAC]",
        "(1920x1080 x265 flac)",
        "10-Bit",
        "YURASUKA",
        "BluRay",
        "FLAC2.0",
        "[Judas]",
        "[Kametsu]",
        "(BD 1080p Hi10 FLACx2)",
        "Hi10",
        "FLACx2",
        "[Nep_Blanc]"
        "MULTI VFF",
        "10Bits",
        "T0M",
        "ETTV",
        "BDRemux",
        "DVD",
        "WEB-DL",
        "ENG",
        "JPN",
        "]"
        "["
        ]

    # List duplication checker :)
    #checkForDups(removeStrings)

    removeStringsSorted = (sorted(removeStrings, key=len, reverse=True))
    #print(removeStringsSorted)

    outputFilename = filename.replace(str(".mkv"), "")

    for item in removeStringsSorted:

        if not outputFilename.find(item)+len(item) == len(item) - 1:
            # covert strings to lowercase, why? because re.sub and []() don't work together
            outputFilenameLower = outputFilename.lower()
            itemLower = item.lower()
            outputFilename = outputFilename[:outputFilenameLower.find(itemLower)] + outputFilename[outputFilenameLower.find(itemLower) + len(item):]


    outputFilename = re.sub("\[[^\[][^\[][^\[][^\[][^\[][^\[][^\[][^\[]\]", "", outputFilename)  # remove e.g.[ABC12345]

    outputFilename = outputFilename.replace("_", " ")  # _ is usally a stand in for space
    outputFilename = outputFilename.replace(" -", " ")
    outputFilename = outputFilename.replace("- ", " ")

    outputFilename = re.sub("\s\s+", " ", outputFilename)  # Make 2 or more continuous spaces into one

    outputFilename = outputFilename.strip()  # Remove leading and trailing whitespaces

    outputFilename = re.sub("\s[0-9][0-9]$", " E"+outputFilename[len(outputFilename) - 2:len(outputFilename)], outputFilename) + ".mkv"  # Add E to episode number and add extension

    #print(outputFilename)

    #return outputFilename

    return outputFilename