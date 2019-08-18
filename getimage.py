#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import math
import configparser

picdir = os.path.join(os.getcwd(), 'pic')
libdir = os.path.join(os.getcwd(), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont

from io import BytesIO
import requests

logging.basicConfig(level=logging.DEBUG)


epd = epd4in2.EPD()

cfg = configparser.ConfigParser()
cfg.read('config.ini')

urlImage = cfg.get('url', 'image')

def loop():
    try:
        logging.info("loop")


        response = requests.get(urlImage)
        img = Image.open(BytesIO(response.content))
        HImage = img.convert('1')

        epd.display(epd.getbuffer(HImage))

        time.sleep(300)
    except IOError as e:
        logging.info(e)
        time.sleep(30)

    except KeyboardInterrupt:
        logging.info("Exit.")
        epd4in2.epdconfig.module_exit()
        exit()

def main():
    logging.info("init")
    epd.init()
    while True:
        loop()

main()
