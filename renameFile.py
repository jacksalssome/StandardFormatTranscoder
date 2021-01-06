import re


def checkForDups(tempList):  # List duplication checker
    seen = {}
    dupes = []
    for x in tempList:
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

    # Need to be able to handle triple digits eg ep 123

    removeStrings = [  # Remove all strings listed (Note: case and order doesn't matter)
        "()",
        "[]",
        "{}",
        "[Web 1080p HEVC Multi]",
        "HR-RG",
        "480p",
        "(Multiple Subtitle)",
        "[Multi-Subs]",
        "Web 1080p",
        "E-OPUS",
        "English-Dub",
        "HR-GZ",
        "HR-DR",
        "HR-SW",
        "[Eng-Subs] - Judas",
        "Eng-Subs",
        "[BluRay 1080p HEVC]",
        "BD1080p",
        "[HEVC-x265]",
        "1080p.WEB.x264",
        "WEB.x264",
        "[BD]",
        "[AAC]",
        "Judas",
        "Erai-raws",
        "[TGx]",
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
        "WEB.h264",
        "h264",
        "h265",
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
        "[720p]",
        "(Dual Audio_10bit_BD1080p_x265)",
        "[Dual Audio 10bit 720p]",
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
        "[HorribleSubs]",
        "[AAC]"
        "ENG",
        "JPN",
        "]"
        "["
        "[~AA~]",
        "[Aeenald]",
        "[ANE]",
        "[AnimeCreed]",
        "[Beatrice-Raws]",
        "[BlurayDesuYo]",
        "[CBM]",
        "[Cerberus]",
        "[Chimera]",
        "[DragsterPS]",
        "[Multi-Audio]",
        "[Edge]",
        "[UNCENSORED BD 1080p]",
        "[HEVC-reencode]",
        "[DVDRip 1280x720 h264 ac3]",
        "DVDRip",
        "[HQR]",
        "[KgOlve]",
        "[KH]",
        "[Kōritsu_bonkai77]",
        "[neoHEVC]",
        "[Ranger]",
        "[Reaktor]",
        "[5.1]",
        "[Shisukon]",
        "[Tsundere]",
        "1024x576",
        "[VCB-Studio]",
        "[Ma10p_1080p]",
        "[Ma10p_720p]",
        "[wat15]",
        "[WBDP]",
        "[1080p-AC3-FLAC]",
        "8-bit FLAC 16-bit",
        "8-bit",
        "16-bit",
        "[ZetaRebel]",
        "720x480",
        "720x480p",
        "[sxales]",
        "(DVDRip 720x480p x265 HEVC AC3x3 2.0x3)",
        "(Hi10)",
        "(DVD_480p)",
        "(Exiled-Destiny)",
        "[Exiled-Destiny]",
        "(10bit_BD720p_x265)",
        "[Prof]",
        "HR-J",
        "[Dual-Audio]",
        "[BD 1080p AAC HEVC 10bit]",
        "[GrimRipper]",
        ".1080p.Blu-Ray.10-Bit.Dual-Audio.DTS-HD.x265",
        "DTS-HD",
        "iAHD",
        "(1080p BluRay x265 RCVR)",
        "(Dual Audio 10bit BD1080p x265)",
        "[Dual]",
        "[Subs]",
        "[HD]",
        "BrRip",
        "[Coalgirls-subs]",
        "Blu-Ray.10-Bit.Dual-Audio.TrueHD.x265",
        "TrueHD",
        "Blu-Ray",
        "[ShowY]",
        "[FFFmpeg]",
        "[BD 1080p HEVC AAC]",
        "[FFF]",
        "[Lazy Lily]",
        "[EMBER]",
        "[Mezashite]",
        "[BD 1080p AAC]",
        "(1080p x265 q22 FS94 Joy)",
        "FLACx2 2.0x2",
        "(Dual Audio)",
        "[cen]",
        "[Complete Subbed]",
        "WEB-720PX",
        "[Shinkiro-raw]",
        "[pkanime]",
        "[hshare.net]",
        "[ENG.SUBS]",
        "[UNCEN]",
        "[960x720]",
        "[EROBEAT]",
        "[UNCUT]",
        "[BDremux]",
        "( HT )",
        "~AA~"
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
            # Beautiful, we don't work on the actual filename, so original uppercase and lowercase is unchanged
            # only subtracting the positions
            outputFilename = outputFilename[:outputFilenameLower.find(itemLower)] + outputFilename[outputFilenameLower.find(itemLower) + len(item):]

    outputFilename = re.sub("\[[^\[][^\[][^\[][^\[][^\[][^\[][^\[][^\[]\]", "", outputFilename)  # remove e.g.[ABC12345]

    outputFilename = outputFilename.replace(".", " ")  # _ is usually a stand in for a space
    outputFilename = outputFilename.replace("_", " ")  # _ is usually a stand in for a space

    outputFilename = re.sub("\([0-9][0-9][0-9][0-9]\)", "", outputFilename)  # Remove Years eg. (1994)

    outputFilename = outputFilename.strip()  # Remove leading and trailing whitespaces

    outputFilename = re.sub(r"ep ([0-9][0-9])", r"E\1", outputFilename, flags=re.I)  # ep 13 to E13
    outputFilename = re.sub(r"ep ([0-9])", r"E0\1", outputFilename, flags=re.I)  # ep 3 to E03

    outputFilename = re.sub(r"ep([0-9][0-9])", r"E\1", outputFilename, flags=re.I)  # ep03 to E03
    outputFilename = re.sub(r"ep([0-9])", r"E0\1", outputFilename, flags=re.I)  # ep3 to E03 Haven't seen one with this case, but il code it in anyway

    outputFilename = re.sub("- ([0-9][0-9][0-9])$", r" E\1 ", outputFilename)  # Replace "- 001" with E001, why would any have so may episodes, IDK
    outputFilename = re.sub("\s([0-9][0-9])\s", r" E\1 ", outputFilename)  # Replace (space + 02 + space) If there are double digits left at is stage this its probably a ep number
    outputFilename = re.sub("-([0-9][0-9])$", r" E\1 ", outputFilename)  # Replace -01 If at end of file name
    outputFilename = re.sub("\[([0-9][0-9])\]", r" E\1 ", outputFilename)  # Replace [01] with E01
    outputFilename = re.sub("([0-9][0-9])x([0-9][0-9])", r" S\1E\2 ", outputFilename)  # 11x01 to S11E01
    outputFilename = re.sub("([0-9])x([0-9][0-9])", r" S0\1E\2 ", outputFilename)  # 1x01 to S01E01

    outputFilename = outputFilename.replace(" -", " ")
    outputFilename = outputFilename.replace("- ", " ")

    outputFilename = re.sub("\s\s+", " ", outputFilename)  # Make 2 or more continuous spaces into one

    outputFilename = re.sub("\s[0-9][0-9]$", " E"+outputFilename[len(outputFilename) - 2:len(outputFilename)], outputFilename) + ".mkv"  # Add E to episode number and add extension

    #print(outputFilename)

    return outputFilename
