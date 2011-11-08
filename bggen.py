#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ubuntu wallpaper slide generator
# Author: Valdir Stumm Junior - stummjr a gmail · com


import os
import sys
import datetime
import argparse
from os import path
from datetime import date


S_TAG = """
    <static>
      <duration>%.1f</duration>
      <file>%s</file>
    </static>"""

T_TAG = """
    <transition>
      <duration>%.1f</duration>
      <from>%s</from>
      <to>%s</to>
    </transition>"""

START_TAG = """
    <starttime>
      <year>%d</year>
      <month>%d</month>
      <day>%d</day>
      <hour>%d</hour>
      <minute>%d</minute>
      <second>%d</second>
    </starttime>"""

BG_OTAG = "<background>"

BG_CTAG = "</background>"


def static_tag(duration, filename):
  return S_TAG % (duration, filename)


def transition_tag(duration, fromfile, tofile):
  return T_TAG % (duration, fromfile, tofile)


def start_tag():
  now = datetime.datetime.now()
  year = now.year
  month = now.month
  day = now.day
  h = now.hour
  m = now.minute
  s = now.second
  return START_TAG % (year, month, day, h, m, s)


def parse_arguments():
  p = argparse.ArgumentParser()
  p.add_argument('-p', action = 'append', dest = 'path', default = [], 
                  help = 'Path to the wallpapers', required = True)
  p.add_argument('-t', dest='duration', default=40, type=int, required=True,
                  help = 'Time (minutes) before changing to next wallpaper.')
  p.add_argument('-o', dest='filename', default='', help='Output filename.')
  args = p.parse_args()
  return args.path, args.duration, args.filename


def expand_path(path_list):
  l = []
  for p in path_list:
    if not p.startswith('/'): # expand relative path
      p = os.getcwd() + '/' + p
    if path.isdir(p):
      l = l + filter(path.isfile, map(lambda x : p + '/' + x, os.listdir(p)))
    elif path.isfile(p):
      l.append(p) # go to the result list
  return l


def format_xml(path_list, duration, filename):
  fout = sys.stdout if filename == '' else open(filename, 'w') 
  if len(path_list) > 0:
    fout.write(BG_OTAG + "\n" + start_tag() + "\n")
    previous = path_list[0]
    for p in path_list[1:]:
      fout.write(static_tag(duration * 60.0, previous) + "\n")
      fout.write(transition_tag(5.0, previous, p) + "\n")
      previous = p
    fout.write(BG_CTAG)
    fout.close()


if __name__ == '__main__':
  path_list, duration, filename = parse_arguments()
  path_list = expand_path(path_list)
  format_xml(path_list, duration, filename)
