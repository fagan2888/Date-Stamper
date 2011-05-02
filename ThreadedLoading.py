from threading import *
from PIL import Image
import Conversions
import Images
import wx
import os

class LoadIms(Thread):

    def __init__(self, frame, id, im, path, imagelist, imList):

        self.frame = frame
        self.im = im
        self.path = path
        self.il = imagelist
        self.imList = imList
        #self.resultFcn = resultFcn
        self.id = id # event identification id

        Thread.__init__(self)

        self.start()

    def run(self):
        """ Perform Threaded Action """

        # get variables here
        path = self.path

        validExt = ["jpg","jpeg"]

        count = 0

        for root, dirs, files in os.walk(path):
            for f in files:
                if(f.lower()[f.rfind(".")+1:] in validExt):
                    self.im.append(Images.loader(root,f))
                    tmpim = Image.open(os.path.join(root,f))
                    tmpim.thumbnail((125,125))
                    tmpim = Conversions.padpiltoimage(tmpim,125,125).ConvertToBitmap()

                    self.il.Add(tmpim)
                    count += 1

                    wx.PostEvent(self.frame,ReturnFunction(count,self.id,0))

        self.imList.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        #self.imList.SetImageList(self.il, wx.IMAGE_LIST_NORMAL)

        self.imList.InsertColumn(0,'',width=130)

        for i in range(count):
            self.imList.InsertStringItem(i,'')
            self.imList.SetItemImage(i,i)

        wx.PostEvent(self.frame, ReturnFunction("Ready...",self.id,1))

class ReturnFunction(wx.PyEvent):

    def __init__(self, data, id,done):

        wx.PyEvent.__init__(self)
        self.SetEventType(id)
        self.data = data
        self.done = done