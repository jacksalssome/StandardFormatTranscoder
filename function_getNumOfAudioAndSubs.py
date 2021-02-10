def findEngSub(outputTable, row):
    outLang = (outputTable.get_string(start=row, end=row + 1, fields=["Language"]).strip()).lower()
    outCodecType = (outputTable.get_string(start=row, end=row + 1, fields=["CodecType"]).strip()).lower()

    if outCodecType == "subtitle" and outLang == "eng":
        return True
    return False

def findSignSong(outputTable, row):
    outLang = (outputTable.get_string(start=row, end=row + 1, fields=["Language"]).strip()).lower()
    outCodecType = (outputTable.get_string(start=row, end=row + 1, fields=["CodecType"]).strip()).lower()

    if outCodecType == "subtitle" and outLang == "SignsSongs":
        return True
    return False


def findJpnAudio(outputTable, row):
    outLang = (outputTable.get_string(start=row, end=row + 1, fields=["Language"]).strip()).lower()
    outCodecType = (outputTable.get_string(start=row, end=row + 1, fields=["CodecType"]).strip()).lower()

    if outCodecType == "audio" and outLang == "jpn":
        return True
    return False


def findEngAudio(outputTable, row):
    outLang = (outputTable.get_string(start=row, end=row + 1, fields=["Language"]).strip()).lower()
    outCodecType = (outputTable.get_string(start=row, end=row + 1, fields=["CodecType"]).strip()).lower()
    outTitle = (outputTable.get_string(start=row, end=row + 1, fields=["Title"]).strip()).lower()

    if outCodecType == "audio" and outLang == "eng" and "commentary" not in outTitle:  # Make sure commentary isn't default if theres a foreign audio and a eng commentary
        return True
    return False
