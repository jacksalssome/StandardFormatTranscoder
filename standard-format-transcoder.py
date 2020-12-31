import os
from pathlib import Path
import shutil
import subprocess
import re

from function_getMetadata import getAndSaveMetadata
from main2 import main2

directory = os.path.dirname(os.path.realpath(__file__))

#print(directory)
#print(os.listdir(directory))

print("Transcode Starting")
Path("MKVoutput/").mkdir(parents=True, exist_ok=True)
Path("Metadata/").mkdir(parents=True, exist_ok=True)

iterations = 0
for filename in os.listdir(directory):
    if filename.endswith(".mkv"):  # Find Any MKV files
        iterations = iterations + 1  # Log how many files we change

        streamNum = 0

        metadataTable, totalNumOfStreams = getAndSaveMetadata(filename)

        # -- Open Metadata file for processing --

        metadataAndMaps = main2(filename, metadataTable, totalNumOfStreams)

        #print("ffmpeg -v error -n -i \""+filename+"\" -map_metadata -1 -map_chapters 0 "+metadataAndMaps+" -metadata title=\"\" -c copy -copy_unknown \"MKVoutput\\"+filename+"\"")

        os.system("cmd /c ffmpeg -v error -n -i \""+filename+"\" -map_metadata -1 -map_chapters 0"+metadataAndMaps+" -metadata title=\"\" -c copy -copy_unknown \"MKVoutput\\"+filename+"\"")


        #print(os.path.join(directory, filename))

        print("Done: " + filename)

# Remove metadata directory

#try:
#    shutil.rmtree("Metadata")
#except OSError as e:
#    print("Error: %s : %s" % ("Metadata", e.strerror))

print("Finished", iterations, "files")
input("Press ENTER to exit...")

