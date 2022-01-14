#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import os
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
from virtual.detect import applyfilter, applyfilteronimage
import time
import json,re
# import cv2

define("port", default=8099, help="run on the given port", type=int)

counter = 0
mask = []
partcolorsdic = {'Crease': 'none', 'LowerLashline': 'none', 'EyeBrows': 'none', 'LipStick': 'none'}
class MainHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("A client connected.")

    def on_close(self):
        logging.info("A client disconnected")

    def on_message(self, message):
        global mask , counter

        s1 = time.time()
        mess = json.loads(message)
        rgbimage = mess["image"]
        opacity = int(mess["opacity"])
        color = mess["color"]
        width = mess["videowidth"]
        height = mess["videoheight"]
        partname = mess["part"]
        # # partname = json_text
        # logging.info("color===="+color+"part== "+partname)
        # partcolorsdic[partname] = color
        # mask = applyfilter(mess["keypoints"])
        # logging.info(partname)
        if counter == 0:
            mask = rgbimage
        elif counter%5  or counter == 1:
            mask = applyfilteronimage(rgbimage,mess["keypoints"],opacity,color,width,height,partname) 
        else:
           mask = mask    
        image_data  = ""
        s2 = time.time()
        logging.info("python time == "+str((s2-s1)*1000))
        counter+=1
        # if not image_data:
        #     image_data = message
        self.write_message(mask)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/websocket", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liveface.settings")
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()