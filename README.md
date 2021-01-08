# StandardFormatTranscoder
<img src="https://github.com/jacksalssome/StandardFormatTranscoder/blob/main/images/SMF.png" alt="SMF logo" width="20%" />
                                                                                                                      
## Overview

* Removes metadata from Video files (currently only .MKV), but leaves track titles with audio channels, so if its 5.1 surround and an english track it will be: English (5.1)

* Automaticly selects a japanese audio track and the "best" english subtitle track

* Leaves video alone, if you give it a MKV(HEVC, ACC and HDMV-PGS) it will just copy them and change the metadata.

* Removes attachments and cover art

Supported platforms:  
Windows  
Linux: coming soon  
MacOs: I dont have a Mac :/

## Installing

* Get the latest release from https://github.com/jacksalssome/standard-format-transcoder/releases and download the .exe
* Have ffmpeg and ffprobe in the system path

To find and install ffmpeg and ffprobe under windows:
1) Download https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2) extract the zip and go into the bin folder, you'll see ffmpeg.exe, ffplay.exe and ffprobe.exe
3) copy ffmpeg.exe and ffprobe.exe to C:\Program Files\ffmpeg
4) Open the start menu and search for SystemPropertiesAdvanced.exe, then click on the "Environment Variables..." button
5) Under "Sytem variables" click on the Path variable, then click the "Edit.." button
6) Click on New and type in "C:\Program Files\ffmpeg" (No Quotes)
8) Log off and back on, ffmpeg should be working now (can test by typing "ffmpeg" in cmd)

 ## How to run

###### The Easy way:  

Double click on the exe if you want to change files in the same directory  
You can then just move the exe around from directory to directory

###### The Standard way:

    > cd <Path where the exe is>
    > StandardFormatTranscoder.exe --input \Path where the files are>

    For Example:

    > cd C:\Users\username\Downloads\
    > StandardFormatTranscoder.exe --input "C:\Users\username\Videos\[ILoveYou] Another Show [BDRip 1920x1080 x264 FLAC]"
    
    Recursive:
    
    > StandardFormatTranscoder.exe -r --input "C:\Users\username\Videos\[ILoveYou] Another Show [BDRip 1920x1080 x264 FLAC]"
    
    Output of SFT will be
    "C:\Users\username\Videos\SFT output: [ILoveYou] Another Show [BDRip 1920x1080 x264 FLAC]"


## Examples

Here is a breakdown of a MKV file showing each video, audio, subtitle and attachments(Usally fonts, or cover art)

    +-------+-----------------Input Preview--+------------+----------+     +-------+------------Output Preview-+------------+----------+
    +-------+---------------------+----------+------------+----------+     +-------+----------------+----------+------------+----------+
    | Index |        title        | language | codec_type | channels |     | Index |     title      | language | codec_type | channels |
    +-------+---------------------+----------+------------+----------+     +-------+----------------+----------+------------+----------+
    |   0   | Encoded by Iloveyou |          |   video    |          |     |   0   |                |          |   video    |          |
    |   1   |                     |   eng    |   audio    |    6     |     |   1   | English (5.1)  |   eng    |   audio    |    6     |
    |   2   | Japanese (Iloveyou) |   jpn    |   audio    |    2     |     |   2   | Japanese (2.0) |   jpn    |   audio    |    2     |
    |   3   |     Signs/Songs     |   eng    |  subtitle  |          |     |   3   | Signs / Songs  |          |  subtitle  |          |
    |   4   |     (Iloveyou)      |   eng    |  subtitle  |          |     |   4   |    English     |   eng    |  subtitle  |          |
    |   5   |       English       |   eng    |  subtitle  |          |     |   5   |    English     |   eng    |  subtitle  |          |
    |   6   |  English [yoyRips]  |   eng    |  subtitle  |          |     |   6   |    English     |   eng    |  subtitle  |          |
    |   7   |                     |          | attachment |          |     +-------+----------------+----------+------------+----------+
    |   8   |                     |          | attachment |          |     
    |   9   |                     |          | attachment |          |     
    |   10  |                     |          | attachment |          |     
    |   11  |                     |          | attachment |          |     
    |   12  |                     |          | attachment |          |     
    |   13  |                     |          | attachment |          |     
    |   14  |                     |          | attachment |          |     
    |   15  |                     |          | attachment |          |     
    +-------+---------------------+----------+------------+----------+     
    
    If theres a conflict, like index 4, 5 and 6, then it will select the second largest subtitle by file size.

Heres some examples of automatic file renaming:

Input: This.Is.A.Show.S01E04.1080p.BluRay.10-Bit.FLAC5.1.x265-ILOVEYOU.mkv  
Output: This Is A Show S01E04.mkv

Input: [ILoveYou] Another Show 02 [BDRip 1920x1080 x264 FLAC] [A1B2C3D4].MKV  
Output: Another Show E02.mkv

Input: [\~IloveYou\~]_A_-_Shows_Title_Here_ep01_[A1B2C3D4].mkv  
Output: A Shows Title Here E01.mkv

Input: [IloveYou] Show Name (2009) - 003.mkv  
Output: Show Name E003.mkv

Input: A-Show! 03 Episode Title! (BD1080p AC3 10bit).mkv  
Output: A-Show! E03 Episode Title!.mkv

So standard formatting for a filename is:  
[Show Title] [Season & Episode] [Episode Title]

# Compiling

I use PyCharm 2020  
pyinstaller  --icon=images\favicon.ico --onefile StandardFormatTranscoder.py
