# standard-format-transcoder
* Removes metadate from Video files (currently only .MKV), but leaves track titles

* Automaticly selects a japanese audio track and the "best" english subtitle track

* Leaves video alone, if you giv it a HEVC, ACC and HDMV-PGS it will just copy them and change the metadata.

Supported platforms:
Windows

How to run:

* Get the latest release from https://github.com/jacksalssome/standard-format-transcoder/releases and download the zip file
* Have python installed
* python dipendacies: ffmpeg-python, prettytable (cmd: python pip install ffmpeg-python prettytable)

1) Move the files (compareSizes.py, function_getMetadata.py, main2.py, renameFile.py and standard_format_transcoder.py)
   to the directory with the video (MKV) files you want to convert
2) Open cmd and cd into the same directory
3) type: python standard_format_transcoder.py
4) The program will start running


Linux: coming soon

MacOs: i dont have a Mac :/
