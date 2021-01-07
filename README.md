# standard-format-transcoder
* Removes metadata from Video files (currently only .MKV), but leaves track titles with audio channels, so if its 5.1 surround and an english track it will be: English (5.1)

* Automaticly selects a japanese audio track and the "best" english subtitle track

* Leaves video alone, if you give it a MKV(HEVC, ACC and HDMV-PGS) it will just copy them and change the metadata.

* Removes attachments and cover art

Supported platforms:
Windows

How to run:

* Get the latest release from https://github.com/jacksalssome/standard-format-transcoder/releases and download the zip file
* Have python installed
* python dipendacies: ffmpeg-python, prettytable (cmd: pip install ffmpeg-python prettytable)

1) Move the files (compareSizes.py, function_getMetadata.py, main2.py, renameFile.py and standard_format_transcoder.py)
   to the directory with the video (MKV) files you want to convert
2) Open cmd and cd into the same directory
3) type: python standard_format_transcoder.py
4) The program will start running


Linux: coming soon

MacOs: i dont have a Mac :/

Examples:

Here is a breakdown of a MKV file showing each video, audio, subtitle and attachments(Usally fonts, or cover art)

    +-------+-----------------Input Preview--+------------+----------+
    +-------+---------------------+----------+------------+----------+
    | Index |        title        | language | codec_type | channels |
    +-------+---------------------+----------+------------+----------+
    |   0   | Encoded by Iloveyou |          |   video    |          |
    |   1   |                     |   eng    |   audio    |    6     |
    |   2   | Japanese (Iloveyou) |   jpn    |   audio    |    2     |
    |   3   |     Signs/Songs     |   eng    |  subtitle  |          |
    |   4   |     (Iloveyou)      |   eng    |  subtitle  |          |
    |   5   |                     |          | attachment |          |
    |   6   |                     |          | attachment |          |
    |   7   |                     |          | attachment |          |
    |   8   |                     |          | attachment |          |
    |   9   |                     |          | attachment |          |
    |   10  |                     |          | attachment |          |
    |   11  |                     |          | attachment |          |
    |   12  |                     |          | attachment |          |
    |   13  |                     |          | attachment |          |
    |   14  |                     |          | attachment |          |
    +-------+---------------------+----------+------------+----------+

And heres the MKV after:

    +-------+------------Output Preview-+------------+----------+
    +-------+----------------+----------+------------+----------+
    | Index |     title      | language | codec_type | channels |
    +-------+----------------+----------+------------+----------+
    |   0   |                |          |   video    |          |
    |   1   | English (5.1)  |   eng    |   audio    |    6     |
    |   2   | Japanese (2.0) |   jpn    |   audio    |    2     |
    |   3   | Signs / Songs  |          |  subtitle  |          |
    |   4   |    English     |   eng    |  subtitle  |          |
    +-------+----------------+----------+------------+----------+

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
