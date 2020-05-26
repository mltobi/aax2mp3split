# aax2mp3split

## Description
This script converts an AAX file to a MP3 file. The MP3 file is split by the detected chapters using _ffprobe_. The split is done using _ffmpeg_ with _segment_times_ option which is much faster then _start/end_ option.

## Usage
```
  usage: aax2mp3split.py [-h] [-af AAXFOLDER] [-sp SPLITPATTERN] [-ac AUTHCODE]

  aax to mp3 converation with chapter split

  optional arguments:
    -h, --help            show this help message and exit
    -af AAXFOLDER, --aaxfolder AAXFOLDER
                          Input folder of AAX files
    -sp SPLITPATTERN, --splitpattern SPLITPATTERN
                          Pattern to split file name for title and album
                          extraction
    -ac AUTHCODE, --authcode AUTHCODE
                          Authorization code, e.g. 1234abcd
```
