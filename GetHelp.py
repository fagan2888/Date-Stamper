import os
import wx
import wx.html
import sys

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()


class DispHelp:
    def __init__(self,crap):

        exedir = os.path.dirname(sys.executable)

        if(os.path.isfile("help.inc")):
            helpText = open('help.inc',"r").read()
        elif(os.path.isfile(os.path.join(exedir,"help.inc"))):
            helpText = open(os.path.join(exedir,"help.inc"),"r").read()
        else:
            helpText = 'Cannot Locate Help File'

        self.hb = wx.Dialog(None, -1, "Date Stamper Help",
        style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)

        hwin = HtmlWindow(self.hb, -1, size=(400,400))

        hwin.SetPage(helpText)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()

        #hwin.SetSize((irep.GetWidth(), int(irep.GetHeight()/4)))
        self.hb.Show(True)
        self.hb.SetClientSize(hwin.GetSize())
        self.hb.CenterOnParent(wx.BOTH)
        self.hb.SetFocus()
        
        self.hb.Bind(wx.EVT_CLOSE, self.hbquit, id=self.hb.GetId())

    def hbquit(self, *evnt):
        self.hb.Destroy()
