from function_compareSizes import compareSizes


def findBestEngSubStream(listOfEngSubs, filename, currentOS):
    biggestStreamSize = 0
    secondBiggestStreamSize = 0
    selBiggestStream = False
    biggestStreamNum = -1
    secondBiggestStreamNum = -1


    for row in listOfEngSubs:  # Start iterating from the first sub

        streamSize = compareSizes(row, filename, currentOS)

        if len(listOfEngSubs) == 2:  # Just select the biggest if theres only 2 subs
            selBiggestStream = True
            if streamSize > biggestStreamSize:
                biggestStreamSize = streamSize
                biggestStreamNum = row

        elif len(listOfEngSubs) >= 3:  # select the second biggest if theres more then 2 subs
            if streamSize > biggestStreamSize:  # If current stream is biggest
                biggestStreamSize = streamSize
            elif streamSize > secondBiggestStreamSize:  # If the current stream is not the biggest, but bigger the the second biggest
                secondBiggestStreamSize = streamSize
                secondBiggestStreamNum = row

    if selBiggestStream is True:
        return biggestStreamNum
    else:
        return secondBiggestStreamNum
