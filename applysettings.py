""" The purpose of this module is to apply a certain images
            font properties to all other images"""

import DateFormat
import wx
import os
import TEXT
import time

from threading import *

from PIL import ImageFont, ImageDraw, Image

class ApplyAll(Thread):

    def __init__(self, frame, id, handle, otherhandles):

        self.handle = handle
        self.otherhandles = otherhandles
        self.id = id
        self.frame = frame

        Thread.__init__(self)

        self.start()

    def run(self):

        attributes = ['format','fontfamily','fontsize',
                  'fontcolor','align','position']

        wx.PostEvent(self.frame, ApplyReturnFunction("Propogating Settings", self.id, 0))

        for key in attributes:

            for im in self.otherhandles:

                if im is not self.handle:

                    im.__dict__[key] = self.handle.__dict__[key]

                    im.font = wx.Font(im.fontsize, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTWEIGHT_NORMAL,wx.FONTSTYLE_NORMAL,
                                  face=im.fontfamily)
                                  
                    year, month, day = im.date
                    im.dateText = DateFormat.Format(int(year), int(month),
                                    int(day), im.format)

        wx.PostEvent(self.frame, ApplyReturnFunction("Ready...", self.id, 1))

class Commit(Thread):

    def __init__(self, frame, id, handles, fonts):

        self.id = id
        self.frame = frame
        self.handles = handles
        self.fonts = fonts

        Thread.__init__(self)

        self.start()

    def run(self):

        count = 1

        for im in self.handles:

            wx.PostEvent(self.frame,
                CommitReturnFunction(im.name + ' (' + str(count) + ' of ', self.id, 0))

            text = im.dateText

            pil = Image.open(im.path)

            ptsize = int(round(im.font.GetPointSize()*pil.size[1]/im.thumbX.size[1]))

            f = ImageFont.truetype(self.fonts[im.font.GetFaceName()],ptsize)

            draw = ImageDraw.Draw(pil)

            position = TEXT.calcXY(draw.textsize(text, font=f),pil.size,im.align,im.position)

            draw.text(position, text, fill=im.fontcolor.GetAsString(flags=wx.C2S_HTML_SYNTAX),
                        font=f)

            del draw

            path = os.path.join(im.rootDir,'Labelled')

            if not os.path.isdir(path):
                os.makedirs(path)

            tmp = im.name.split('.')
            tmp.insert(-1,"_dl.")

            filename = ''.join(tmp)

            filename = os.path.join(path,filename)

            pil.save(filename, "JPEG", quality=95)

            count += 1



        wx.PostEvent(self.frame, CommitReturnFunction("COMPLETE!", self.id, 1))

        time.sleep(1)

        wx.PostEvent(self.frame, CommitReturnFunction("Ready...", self.id, 2))


class ApplyReturnFunction(wx.PyEvent):
    """ This one will return data with the counter """

    def __init__(self, data, id, done):

        wx.PyEvent.__init__(self)
        self.SetEventType(id)
        self.data = data
        self.done = done

class CommitReturnFunction(wx.PyEvent):
    """ This one will return data with the Image Name """

    def __init__(self, data, id, done):

        wx.PyEvent.__init__(self)
        self.SetEventType(id)
        self.data = data
        self.done = done