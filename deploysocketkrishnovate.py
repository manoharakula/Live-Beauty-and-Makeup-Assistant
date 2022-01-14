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
import ssl
mask = []
counter = 0
define("port", default=12345, help="run on the given port", type=int)
partcolorsdic = {'Crease': 'none', 'LowerLashline': 'none', 'EyeBrows': 'none', 'LipStick': 'none'}
class MainHandler(tornado.websocket.WebSocketHandler):
    @classmethod
    def route_urls(cls):
        return [(r'/echo',cls, {}),]

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
        # logging.info("python time == "+str((s2-s1)*1000))
        counter+=1
        # if not image_data:
        #     image_data = message
        self.write_message(mask)


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liveface.settings")
    tornado.options.parse_command_line()
    
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain("/home/crazy/virtualmakeupassistant/private/fullchain.pem",
                        "/home/crazy/virtualmakeupassistant/private/privkey.pem")
    http_server = tornado.httpserver.HTTPServer(tornado.web.Application(MainHandler.route_urls()), ssl_options=ssl_ctx)


    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
