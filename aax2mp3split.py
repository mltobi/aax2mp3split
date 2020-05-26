#!/usr/bin/python3

import sys
import os
import shutil
import glob
import subprocess
import json
import argparse


def getMediaData(filename, auth_code=None):
  chapters=[]

  cmd = ['ffprobe', '-i', filename, '-print_format', 'json', '-show_format', '-show_chapters', '-loglevel', 'error']
  if auth_code != None:
    cmd.append('-activation_bytes')
    cmd.append(auth_code)

  process = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding="utf-8")
  sout = process.stdout.read()

  return json.loads(sout)


def convMp3(aaxfile, mp3file, auth_code, mediadata):

  title = mediadata['format']['tags']['title']
  artist = mediadata['format']['tags']['artist']
  album_artist = mediadata['format']['tags']['album_artist']
  album = mediadata['format']['tags']['album']
  album_date = mediadata['format']['tags']['date']
  genre = mediadata['format']['tags']['genre']

  bitrate = mediadata['format']['bit_rate']
  codec = 'libmp3lame'
  container = 'mp3'

  cmd = ['ffmpeg', '-loglevel', 'error', '-stats',
         '-activation_bytes', auth_code,
         '-i', aaxfile,
         '-vn', '-codec:a', codec, '-ab', bitrate,
         '-map_metadata', '-1',
         '-metadata', 'title=%s' % (title),
         '-metadata', 'artist=%s' % (artist),
         '-metadata', 'album_artist=%s' % (album_artist),
         '-metadata', 'album=%s' % (album),
         '-metadata', 'date=%s' % (album_date),
         '-metadata', 'track=1/1',
         '-metadata', 'genre=%s' % (genre),
         '-metadata', 'copyright=%s' % (copyright),
         '-f', container, mp3file]

#         '-t', '600',

  process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  process.wait()


def splitMp3(mp3file, mediadata, title, album):

  folder = album

  seg_times = ''
  for chap in mediadata['chapters']:
    seg_times = '%s,%s' % (seg_times, chap['start_time'])

  seg_times = seg_times[1:]

  basefolder = os.path.dirname(mp3file)
  outfolder = os.path.abspath('%s/%s - %s' % (basefolder, folder, title))

  if os.path.exists(outfolder):
    shutil.rmtree(outfolder)
  os.mkdir(outfolder)

  cmd = ['ffmpeg', '-loglevel', 'error', '-stats', '-i', mp3file, '-f', 'segment', '-segment_times', seg_times, '-c', 'copy', '-map', '0', '%s/%s - %%03d.mp3' % (outfolder, title)]
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  process.wait()



if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='aax to mp3 converation wiht chapter split')

  parser.add_argument('-af',  '--aaxfolder',    help = 'Input folder of AAX files', default = './')
  parser.add_argument('-sp',  '--splitpattern', help = 'Pattern to split file name for title and album extraction', default = '###')
  parser.add_argument('-ac',  '--authcode',     help = 'Authorization code, e.g. 1234abcd', default = None)
  args = parser.parse_args()

  if args.authcode == None:
    print('No Authorization code provided: use --authcode 1234abcd')
    sys.exit()

  aaxs = glob.glob(args.aaxfolder + '/*.aax')
  AXXs = glob.glob(args.aaxfolder + '/*.AAX')
  aaxfiles = aaxs + AAXs

  if aaxfiles != []:

    print('Found AAX files:')
    for aaxfile in aaxfiles:
      print('  - %s' % aaxfile)

    mp3file = os.path.dirname(aaxfiles[0]) + '/tmp.mp3'

    for aaxfile in aaxfiles:
      if os.path.exists(mp3file):
        os.remove(mp3file)

      print('Process: "%s"' % aaxfile)

      print('  AAX media data...')
      data = getMediaData(aaxfile, args.authcode)
      print('  AAX to MP3...')
      convMp3(aaxfile, mp3file, args.authcode, data)

      print('  MP3 media data...')
      data = getMediaData(aaxfile, args.authcode)

      print('  MP3 split...')
      parts = os.path.basename(aaxfile).split(' %s ' % args.splitpattern)
      title = parts[0]
      album = args.splitpattern + ' ' + parts[1].split('.')[0]
      splitMp3(mp3file, data, title, album)
      print('')

  else:
   print('Kein "aax" Dateien gefunden!')
