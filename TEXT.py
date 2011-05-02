import wx

__author__="suever"
__date__ ="$Feb 23, 2009 8:51:50 PM$"

def write(text, bitmap, align, font, color, pos=(10,10)):
    """ Writes the supplied text to the image using MemoryDC"""

    memory = wx.MemoryDC()

    memory.SetTextForeground(color)
    memory.SetFont(font)

    memory.SelectObject(bitmap)
    
    x,y = calcXY(memory.GetTextExtent(text),bitmap.Size,align,pos)
    memory.DrawText(text,x,y)

    return bitmap

def calcXY(textsize,imsize,alignment,offsets):

    imsz = min(imsize)

    if(alignment[0] == 0):
        x = offsets[0]*imsize[0]/100
    else:
        x = imsize[0]-textsize[0]-(offsets[0]*imsz/100)
    if(alignment[1] == 0):
        y = offsets[1]*imsize[1]/100
    else:
        y = imsize[1]-textsize[1]-(offsets[1]*imsz/100)

    return x,y

def fontProps(memory, font=None, color=None):
    """ Sets the Properties to be used by the Font """

    if font:
        memory.SetFont(font)
    else:
        font = wx.Font(12,wx.FONTFAMILY_SWISS, wx.FONTWEIGHT_NORMAL,
            wx.FONTSTYLE_NORMAL)
        memory.SetFont(font)
    if color:
        memory.SetTextForeground(color)
        