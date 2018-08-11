#!/usr/bin/env python

from time import clock, sleep
from subprocess import check_output, call, STDOUT
from PIL import Image
import re
import os
import glob

FNULL = open(os.devnull, 'w')
DEBUG = False
default_path = '/Users/julianyocum/Documents/Projects/Neural_Network/data/img_stream/'

#call this to capture image
def capture(path=default_path):
  check_for_device()
  clock()
  screen_on()
  delete_photos()
  open_camera()
  press_camera_button()
  transfer_img(path)
  image = open_file()

  return image

def check_for_device():
    pass
    
def screen_on():
  # check screen on/off state: adb shell dumpsys power | grep state --> Display Power: state=OFF\r\r or ON\r\r
  if DEBUG: print 'screen_on'.ljust(20), clock()
  r = check_output(['adb','shell','dumpsys','power'])
  try:
    state = re.search('Display Power: state=(.*)',r).group(1)
  except AttributeError:
    state = 'Unknown'

  ## DEBUG print 'state is',repr(state)
  # if OFF turn it on: adb shell input keyevent = POWER
  if state.strip() == 'OFF':
    r = check_output(['adb','shell','input','keyevent = POWER', '&&', 'input', 'touchscreen', 'swipe', '930', '880', '930', '380'])
    if DEBUG: print r.strip()

def open_camera():
  # check if camera is the top most: adb shell dumpsys activity activities | grep mFocusedActivity --> mFocusedActivity: ActivityRecord{f9da72a u0 com.sec.android.app.camera/.Camera t3967}
  if DEBUG: print 'open_camera'.ljust(20), clock()
  r = check_output(['adb','shell','dumpsys','activity','activities'])

  try:
    app = re.search('mFocusedActivity(.*)',r).group(1)
  except AttributeError:
    app = 'Unknown'
  
  # if not open camera app:adb shell am start -a android.media.action.IMAGE_CAPTURE
  if not 'com.sec.android.app.camera' in app:
    r = check_output(['adb','shell','monkey','-p',
        'com.sec.android.app.camera','-c', 'android.intent.category.LAUNCHER', '1'])

    sleep(2)

    call(['adb','shell','input','keyevent = VOLUME_UP'
          ,'input','keyevent = VOLUME_UP'
          ,'input','keyevent = VOLUME_UP'
          ,'input','keyevent = VOLUME_UP'
          ,'input','keyevent = VOLUME_UP'
          ,'input','keyevent = VOLUME_UP'])

    if DEBUG: print r.strip()
#sleep(2)

def delete_photos():
  #delete from phone: adb shell rm /sdcard/DCIM/Camera/*
  if DEBUG: print 'clear_camera_folder'.ljust(20), clock()
  r = check_output(['adb','shell','cd', '/storage/sdcard0/DCIM/Camera/', '&&', 'rm', '*'])
  if DEBUG: print r.strip()

def press_camera_button():
  #condition 1 screen on 2 camera open: adb shell input keyevent = CAMERA
  if DEBUG: print 'press_camera_button'.ljust(20), clock()


  call(['adb', 'shell', 'input', 'touchscreen', 'tap', '850', '550'])
  sleep(3)

  call(['adb','shell','input','keyevent = CAMERA'])
  sleep(2)
  
def transfer_img(path):
  #looking for last file in DCIM/Camera: NO NEED cause we just have 1 picture (clear folder before capture)
  #copy to PC: adb pull /sdcard/DCIM/Camera/ c:/temp
  if DEBUG: print 'screen transfer_img'.ljust(20), clock()
  #r = check_output(['$(adb','pull','/storage/sdcard0/DCIM/Camera/', path, ')', '&>/dev/null'])
  call(['adb','pull','/storage/sdcard0/DCIM/Camera/', path], stdout=FNULL, stderr=STDOUT)

  if DEBUG: print r.strip()

def open_file():
  fl = glob.glob('../data/img_stream/*.jpg')

  try:
    last_file = max(fl, key=os.path.getctime)
  except ValueError:
    print "Image capture failed"
    exit()

  im = Image.open(last_file)

  return im



if __name__ == "__main__":
    import sys

    DEBUG = True

    if len(sys.argv) == 2:
        capture(sys.argv[1])
    elif len(sys.argv) == 1:
        capture()
    else:
        print "Usage:  ./collector.py [path_for_image]"
