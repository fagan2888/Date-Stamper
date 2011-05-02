import EXIF
from PIL import Image
#import re
import os
import wx
import TEXT
import Conversions
import time
import DateFormat
import Configx

__author__="suever"
__date__ ="$Feb 23, 2009 8:27:06 PM$"

class loader:
    """Image class to handle each of the images to be included"""

    def __init__(self, rootDir, filename):

        defaults = Configx.Creator().readDefaults()

        self.rootDir = rootDir

        self.path = os.path.join(rootDir,filename)
        self.name = filename

        self.thumbX = self.CreateThumb(350)
        self.date = self.GetDate()

        self.format = defaults['format']

        self.dateText = self.SetDateFormat(defaults['format'])

        # Need to implement the option to pull this from default.cfg
        r,g,b = defaults['color']
        self.fontcolor = wx.Color(r,g,b)
        #self.SetAlignment(align=3,update=0)
        self.align = defaults['align']
        self.fontsize = defaults['fontsize']

        self.fontfamily = defaults['fontfamily']

        self.font = wx.Font(self.fontsize,wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL,
            wx.FONTSTYLE_NORMAL, face=self.fontfamily)
        #self.font.SetPixelSize(self.fontsize*list(self.thumbX.size)[1]/100)

        #self.fontfamily = self.font.GetFaceName()

        self.position = defaults['offsets']

    def __setattr__(self,attr,val):
        self.__dict__[attr] = val

    def __getattr(self,attr):
        return self.__dict__[attr]

    def SetPixelFont(self, fontsize):
        """ Change the size of the font in pixels """

        self.fontsize = fontsize
        
        self.font.SetPixelSize((0,self.fontsize*self.thumbX.size[1]/100))


    def CreateThumb(self, tsize):
        
        im = Image.open(self.path)
        im.thumbnail((tsize,tsize))

        return im


    def GetDate(self):
        """ Retrieve the Date from EXIF Data """
        
        f = open(self.path,'rb')

        try:
            rawDate = EXIF.process_file(f)
            rawDate = str(rawDate['Image DateTime'])
            rawDate = rawDate[:10]
            rawDate = rawDate.split(':')
        except:
            rawDate = time.localtime()[0:3]

        return rawDate

    def SetDate(self,datestring):
        """ Used if the user defines the date manually """

        # Check the format

        # We want to keep the original in tact in case we want to revert
        #self.dateText = self.SetDateFormat(0,datestring)
        pass


    def SetDateFormat(self, format):
        """ Set the format used for the date """

        self.format = format

        year, month, day = self.date

        dateText = DateFormat.Format(int(year), int(month), int(day), format)
        
        #if(format == 0):
        #    dateText = '/'.join([month,day,year])

        return dateText

    def SetPosition(self, position=None, update=False):
        """ Allows us to set the position of text """

        if position: self.position = position

        if(update):
            self.updateIm()

    def SetFontColor(self, color):
        """ Just updates the color instead of doing everything else """
        self.fontcolor = color

    def SetFont(self, family):
        """ Set the Font Object """

        #if(size): self.fontsize = size
        if(family): self.fontfamily = family

        self.font = wx.Font(self.fontsize, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL,
            wx.FONTSTYLE_NORMAL,face=self.fontfamily)

    def Update(self, bitmapHandle=None, listing=None):
        """ Updates the Labelled Image using the current parameters and
            Listing is a tuple that provides the imlist handle and index"""

        bmp = Conversions.piltoimage(self.thumbX.copy()).ConvertToBitmap()
        bmp = TEXT.write(self.dateText,bmp,self.align,self.font,self.fontcolor,self.position)

        if(bitmapHandle):
            bitmapHandle.SetBitmap(bmp)
            bitmapHandle.Center()
            bitmapHandle.Refresh()
        else:
            return bmp


    def UpdateImListIms(self):
        pass

    def SetAlignment(self, align, update=1):
        """ Set the horizontal and vertical alignments of the date """

        if(align == 1):
            self.align = wx.ALIGN_LEFT|wx.ALIGN_TOP
        elif(align == 2):
            self.align = wx.ALIGN_CENTER|wx.ALIGN_TOP
        elif(align == 3):
            self.align = wx.ALIGN_RIGHT|wx.ALIGN_TOP
        elif(align == 4):
            self.align = wx.ALIGN_LEFT|wx.ALIGN_CENTER
        elif(align == 5):
            self.align = wx.ALIGN_RIGHT|wx.ALIGN_CENTER
        elif(align == 6):
            self.align = wx.ALIGN_LEFT|wx.ALIGN_BOTTOM
        elif(align == 7):
            self.align = wx.ALIGN_CENTER|wx.ALIGN_BOTTOM
        else:
            self.align = wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM

        # Update is a binary value that specifies whether we are going to reload
        if(update):
            self.Update()