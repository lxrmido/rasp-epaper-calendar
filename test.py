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

cfg = configparser.ConfigParser()
cfg.read('config.ini')

urlTempRange = cfg.get('url', 'temp_range')
urlForecast = cfg.get('url', 'forecast')

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
        draw.text((220, 120), u'{}{} {}'.format(ln.getCnMonth(dt), ln.getCnDay(dt), ln.getUpperWeek(dt)), font = font22, fill = 0)
        # temp
        # draw.line((48, 160, 352, 160), fill = 0)
        # draw.line((48, 290, 352, 290), fill = 0)

        # draw.rectangle((12, 160, 392, 290), outline = 0)

        tempData = getTempData()
        if tempData:
            tempGraph = drawTempGraph(400, 140, tempData)
            Himage.paste(tempGraph, (0, 160))
            draw.text((12, 140), u'{:.1f}℃'.format(max(tempData) / 1000), font = font20, fill = 0)
            draw.text((12, 270), u'{:.1f}℃'.format(min(tempData) / 1000), font = font20, fill = 0)

        forecastData = getForecastData()
        if forecastData:
            draw.text((12, 15), u'今：{} - {}℃'.format(forecastData[0]['tmp_min'], forecastData[0]['tmp_max']), font = font18, fill = 0)
            draw.text((12, 45), u'    {} / {}'.format(forecastData[0]['cond_txt_d'], forecastData[0]['cond_txt_n']), font = font18, fill = 0)
            draw.text((12, 75), u'明：{} - {}℃'.format(forecastData[1]['tmp_min'], forecastData[1]['tmp_max']), font = font18, fill = 0)
            draw.text((12, 105), u'    {} / {}'.format(forecastData[1]['cond_txt_d'], forecastData[1]['cond_txt_n']), font = font18, fill = 0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(180)
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
    length = len(data)
    calcData = []
    if length > width:
        tempsPerPixel = int(math.floor(length / width))
        cx = 0
        while cx <= width:
            avgTemp = 0
            subGroup = data[cx * tempsPerPixel:cx * tempsPerPixel + tempsPerPixel]
            if len(subGroup) > 0:
                avgTemp = int(sum(subGroup) / len(subGroup))
                calcData.append(avgTemp)
            cx += 1
    else:
        tempsPerPixel = 1
        calcData = data
    maxTemp = max(calcData)
    minTemp = min(calcData)
    scaleY = height / (maxTemp - minTemp)
    points = []
    for x, temp in enumerate(calcData):
        points.append((x, int(scaleY * (maxTemp - temp))))
    draw.line(points, fill=0)
    return canvas
        

def getTempData():
    try:
        response = requests.get(urlTempRange)
        dataArray = json.loads(response.text)
    except:
        logging.info("Get temp data failed")
        return False
    else:
        return dataArray

def getForecastData():
    try:
        response = requests.get(urlForecast)
        resData = json.loads(response.text).get('HeWeather6')[0]['daily_forecast']
    except:
        logging.info("Get forecast data failed")
        return False
    else:
        return resData

def main():
    logging.info("init")
    epd.init()
    logging.info("Clear")
    epd.Clear()

    loop()

main()
