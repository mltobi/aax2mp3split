# aax2mp3split

## Description
This script converts AAX files to a MP3 files. It searches recrusively for all AAX files of a defined path.

The MP3 files are split by the detected chapters using _ffprobe_. 
```
ffprobe -i filename -print_format json -show_format -show_chapters -loglevel error
```
The split is done using _ffmpeg_ with _segment_times_ option which is much faster then _start/end_ option.
```
ffmpeg -loglevel error -stats -i mp3file -f segment -segment_times 0, 10, 20 -c copy -map 0 album/title%%03d.mp3
```

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

## Example
```
pi@hostname:~/github/aax2mp3split $ ./aax2mp3split.py --aaxfolder /media/dvr --authcode abcf1234
Found AAX files:
  - /media/dvr/file1.AAX
  - /media/dvr/file2.AAX
Process: "/media/dvr/file1.AAX"
  AAX media data...
  AAX to MP3...
size=  184832kB time=03:17:12.94 bitrate= 128.0kbits/s speed=26.7x
  Split MP3...
...
```
