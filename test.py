#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import math

picdir = os.path.join(os.getcwd(), 'pic')
libdir = os.path.join(os.getcwd(), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont

from datetime import datetime
from lunar import lunar

import requests
import json

logging.basicConfig(level=logging.DEBUG)

font96 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 96)
font80 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 80)
font72 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 72)
font64 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 64)
font56 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 56)
font48 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 48)
font36 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 36)
font24 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 24)
font22 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 22)
font20 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 20)
font18 = ImageFont.truetype(os.path.join(picdir, 'SourceHanSans-Normal.ttc'), 18)
    
epd = epd4in2.EPD()

def loop():
    try:
        logging.info("loop")
        Himage = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(Himage)
        # date
        dt = datetime.now()
        ln = lunar()
        draw.text((236, -10), '{}'.format(dt.day), font = font96, fill = 0)
        draw.text((350, 70), u'{}月'.format(dt.month), font = font22, fill = 0)
        draw.text((205, 120), u'{}{}{}'.format(ln.getCnYear(dt), ln.getCnMonth(dt), ln.getCnDay(dt)), font = font22, fill = 0)
        # temp
        # draw.line((48, 160, 352, 160), fill = 0)
        # draw.line((48, 290, 352, 290), fill = 0)

        # draw.rectangle((12, 160, 392, 290), outline = 0)

        tempData = getTempData()
        if tempData:
            tempGraph = drawTempGraph(380, 130)
            draw.paste(tempGraph(12, 160))

        epd.display(epd.getbuffer(Himage))
        time.sleep(10)
        loop()
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("Exit.")
        epd4in2.epdconfig.module_exit()
        exit()

def drawTempGraph(width, height, data):
    canvas = Image.new('1', (width, height), 255)
    draw = ImageDraw.Draw(canvas)
    maxTemp = max(data)
    minTemp = min(data)
    length = len(data)
    scaleY = height / (maxTemp - minTemp)
    calcData = []
    logging.info('Data: {}, {}'.format(length, scaleY))
    if length > width:
        tempsPerPixel = int(math.floor(length / width))
        cx = 0
        while cx <= width:
            avgTemp = 0
            subGroup = data[x * tempPerPixel:x * tempPerPixex + tempPerPixel]
            if len(subGroup) > 0:
                avgTemp = int(sum(subGroup) / len(subGroup))
                calcData.append(avgTemp)
            cx += 1
    else:
        tempsPerPixel = 1
        calcData = data
    points = []
    for x, temp in calcData:
        points.append((x, int(scaleY * (temp - minTemp))))
    draw.point(points, fill=0)
    return canvas
        

def getTempData():
    try:
        response = requests.get('http://192.168.99.4:4001/range')
        dataArray = json.loads(response.text)
    except:
        logging.info("Get temp data failed")
        return false
    else:
        return dataArray

def main():
    logging.info("init")
    epd.init()
    logging.info("Clear")
    epd.Clear()

    loop()

main()