import os
import wx
from threading import *
import AdvancedSplash
from wx import calendar
import applysettings
import FontFinder
import Configx
import ThreadedLoading
import MenuCreator
import sys

class DatePicker(wx.Frame):

    def __init__(self, handle, bitmaphandle, formathandle, listener, ndx):

        wx.Frame.__init__(self,None,-1, "Select Date", size=(250,250))
        self.dp = calendar.CalendarCtrl(self, -1, pos=(0,10))
        self.Bind(calendar.EVT_CALENDAR_DAY,self.OnDateSelected,self.dp)

        self.handle = handle # This is the handle to the current image

        self.imbmp = bitmaphandle
        self.fh = formathandle
        self.listener = listener
        self.ndx = ndx

        self.SetInitialSize()
        self.CenterOnParent()
        self.Show()

    def OnDateSelected(self, *evnt):
        date = str(self.dp.GetDate())[0:8]
        self.Destroy()
        month,day,year = date.split('/')
        date = map(int,[year,month,day])

        self.handle.date = date
        result = self.handle.SetDateFormat(self.fh.GetSelection())
        self.listener(self.handle,['dateText',],[self.handle.dateText,],[result,],self.ndx)

class ColorPicker:

    def __init__(self, parent):

        dlg = wx.ColourDialog(parent)
        dlg.CenterOnParent()

        if(dlg.ShowModal() == wx.ID_OK):
            self.data = dlg.GetColourData()
        else:
            self.data = None

        dlg.Destroy()

class Main(wx.Frame):

    def __init__(self, parent, id, title):

        self.exedir = os.path.dirname(sys.executable)

        # Prepare the listener for the undo/redo
        self.history = list()
        self.future = list()

        wx.Frame.__init__(self, parent, -1, title, size=(640,590))
        
        sb = self.CreateStatusBar(2)
        sb.SetStatusWidths([-1, 200])
        self.SetStatusText("Please Select A Directory of Images...")

        self.Connect(-1,-1, LOAD_EVT_ID, self.LoadResult)
        self.Connect(-1,-1, COMMIT_EVT_ID, self.CommitResult)
        self.Connect(-1,-1, APPLY_EVT_ID, self.ApplyResult)

#        WHITE_ID = wx.NewId()
#        BLACK_ID = wx.NewId()
#
#        self.Connect(-1,-1, WHITE_ID, self.ColorWhite)
#        self.Connect(-1,-1, BLACK_ID, self.ColorBlack)

        self.Bind(wx.EVT_CLOSE, self.onQuit,id=self.GetId())

#        self.SetAcceleratorTable(wx.AcceleratorTable(
#            [(wx.ACCEL_CTRL, ord('w'), WHITE_ID),
#             (wx.ACCEL_CTRL, ord('k'), BLACK_ID)]))

        if(os.path.isfile(os.path.join('icons','icon.ico'))):
            self.SetIcon(wx.Icon(os.path.join('icons','icon.ico'),wx.BITMAP_TYPE_ICO,16,16))
        elif(os.path.isfile(os.path.join(self.exedir,'icons','icon.ico'))):
            self.SetIcon(wx.Icon(os.path.join(self.exedir,'icons','icon.ico'),wx.BITMAP_TYPE_ICO,16,16))

        self.panel = wx.Panel(self, -1)

        # Create the menu
        self.menubar = MenuCreator.Create(self)
        
        self.initToolbar()
        
        self.imPanel = wx.Panel(self.panel, -1,style=wx.NO_BORDER,size=(360,360))
        self.box = wx.StaticBox(self.panel, -1, "Preview",size=(370,370))
        self.imbmp = wx.StaticBitmap(self.imPanel, -1, 
            wx.EmptyImage(1,1).ConvertToBitmap(),style=wx.NO_BORDER)
            
        self.imList = wx.ListCtrl(self.panel, -1, size=(150,300),
            style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_HRULES |
            wx.LC_ALIGN_TOP | wx.LC_SINGLE_SEL)

        self.il = wx.ImageList(125,125)
        self.imList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.listClick, self.imList)
        self.lbLabel = wx.StaticText(self.panel, -1, "Available Images")
        self.manageLayout()
        self.Center(wx.BOTH)

    def keyPressFcn(self, event):

        print "here"

        keycode = event.KeyCode()

        print keycode

    def ApplyResult(self, event):
        
        if(event.done):
            self.SetStatusText(event.data)
        else:
            self.SetStatusText(event.data)

    def CommitResult(self, event):

        if(event.done == 2):
            self.SetStatusText(event.data)
        elif(event.done == 1):
            self.SetStatusText(event.data)
        else:
            self.SetStatusText("Saving " + event.data + str(len(self.im)) +')')

    def LoadResult(self, event):

        if(event.done):
            self.SetStatusText(event.data)
            self.Enablers()

            self.ndx = 0
            self.im[0].Update(self.imbmp)
            self.updateControls(self.im[0])

        else:
            self.SetStatusText("Processing Image..." + str(event.data))

    def listener(self, index, property, old, new, ndx):

        self.history.append([index, property, old, new, ndx])

        if(len(self.history) > 25):
            self.history = self.history[1:]

        self.future = list()


        self.toolbar.EnableTool(self.toolRedo.GetId(),False)
        self.menubar.redo.Enable(False)
        self.toolbar.EnableTool(self.toolUndo.GetId(),True)
        self.menubar.undo.Enable(True)


        for i in range(len(property)):
            index.__setattr__(property[i],new[i])

        index.Update(self.imbmp)

    def UndoChange(self, *evnt):

        if(len(self.history)):
            if(len(self.history) == 1):
                self.toolbar.EnableTool(self.toolUndo.GetId(),False)
                self.menubar.undo.Enable(False)
            self.toolbar.EnableTool(self.toolRedo.GetId(),True)
            self.menubar.redo.Enable(True)
            change = self.history.pop(-1)
            for i in range(len(change[1])):
                change[0].__setattr__(change[1][i],change[2][i])

            self.future.append([change[0],change[1],change[3],change[2],change[4]])
            self.im[self.ndx].Update(self.imbmp)

            self.updateControls(change[0])
            self.imList.Select(change[-1])

            change[0].Update(self.imbmp)

            self.ndx = change[-1]

    def RedoChange(self, *evnt):
        if(len(self.future)):
            if(len(self.future) == 1):
                self.toolbar.EnableTool(self.toolRedo.GetId(),False)
                self.menubar.redo.Enable(False)
            change = self.future.pop(-1)
            for i in range(len(change[1])):
                change[0].__setattr__(change[1][i],change[2][i])
            self.history.append([change[0],change[1],change[3],change[2],change[4]])
            self.toolbar.EnableTool(self.toolUndo.GetId(),True)
            self.menubar.undo.Enable(True)
            self.im[self.ndx].Update(self.imbmp)

            self.updateControls(change[0])
            self.imList.Select(change[-1])

            change[0].Update(self.imbmp)

            self.ndx = change[-1]

    def initializeMenu(self):
        pass

    def about(self, *evnt):
        description = ''.join(["Program to retrieve date from an image's\n",
                                "EXIF data. It can then display the date\n",
                                "depending on the font and location specified\n",
                                "by the user."])

        info = wx.AboutDialogInfo()

        if(os.path.isfile(os.path.join('icons','icon.ico'))):
            info.SetIcon(wx.Icon(os.path.join('icons','icon.ico'),
                wx.BITMAP_TYPE_ICO))
        elif(os.path.isfile(os.path.join(self.exedir,'icons','icon.ico'))):
            info.SetIcon(wx.Icon(os.path.join(self.exedir,'icons','icon.ico'),
                wx.BITMAP_TYPE_ICO))

        info.SetName('Date Stamper')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2009 Jonathan Suever')
        info.SetWebSite('http://www.suever.net')

        wx.AboutBox(info)

    def updateOffset(self, *evnt):

        curim = self.im[self.ndx]
        self.listener(curim,['position',],[curim.position,],
                     [(self.offsetx.GetValue(), self.offsety.GetValue()),], self.ndx)

    def fontSizeSelect(self, *evnt):
        """ callback for font size spin control """

        curim = self.im[self.ndx]
        sz = curim.font.GetPointSize()
        old = wx.Font(curim.font.GetPointSize(),curim.font.GetFamily(),
                      curim.font.GetWeight(),curim.font.GetStyle(),
                      face=curim.font.GetFaceName())
        curim.font.SetPointSize(self.size.GetValue())

        self.listener(curim,['font','fontsize'],[old,sz],
                     [curim.font,curim.font.GetPointSize()],self.ndx)
        
    def fontSelect(self, *evnt):
        """ Callback for Font Selection """

        curim = self.im[self.ndx]

        ff = self.im[self.ndx].fontfamily

        old = wx.Font(curim.font.GetPointSize(),curim.font.GetFamily(),
                      curim.font.GetWeight(),curim.font.GetStyle(),
                      face=curim.font.GetFaceName())

        nff = self.font.GetStringSelection()

        curim.font.SetFaceName(nff)

        self.listener(curim,['font','fontfamily'],[old,ff],[curim.font,nff],self.ndx)
            
    def manageToolLayout(self, font):
           
        hb1 = wx.BoxSizer(wx.HORIZONTAL)
        
        hb1.Add(font, 0, wx.ALIGN_LEFT | wx.RIGHT, 10)
        hb1.Add(font.cb, 0, wx.ALIGN_LEFT | wx.RIGHT, 20)
        hb1.Add(font.sizeText, 0, wx.ALIGN_LEFT | wx.RIGHT, 10)
        hb1.Add(font.sc, 0, wx.ALIGN_LEFT | wx.RIGHT, 10)
        hb1.Add((0,0), 1, wx.EXPAND)
        hb1.Add(font.colors, 0, wx.ALIGN_RIGHT)
        
        hb2 = wx.BoxSizer(wx.HORIZONTAL)
        
        hb2.Add(font.placementText, 0, wx.ALIGN_LEFT | wx.RIGHT, 10)
        hb2.Add(font.placement, 0, wx.ALIGN_LEFT | wx.RIGHT, 10)
        hb2.Add(font.offsetText, 0, wx.ALIGN_LEFT | wx.RIGHT, 10)
        hb2.Add(font.offsetxText, 0, wx.ALIGN_LEFT)
        hb2.Add(font.offsetx, 0, wx.ALIGN_LEFT | wx.RIGHT, 10)
        hb2.Add(font.offsetyText, 0, wx.ALIGN_LEFT)
        hb2.Add(font.offsety, 0, wx.ALIGN_LEFT | wx.RIGHT, 10)
        hb2.Add((0,0), 1, wx.EXPAND)
        hb2.Add(font.dateFormat, 0, wx.ALIGN_RIGHT)
        
        self.toolsizer = wx.BoxSizer(wx.VERTICAL)
        
        self.toolsizer.Add((0,0), 1, wx.EXPAND)
        self.toolsizer.Add(hb1, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 5)
        self.toolsizer.Add(hb2, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM, 5)

        return

    def ExportChanges(self, *evnt):
        applysettings.Commit(self, COMMIT_EVT_ID, self.im, self.systemFonts)


    def UpdateAlignment(self, evnt, tool):

        try:                
            self.listener(self.im[self.ndx],['align',],[self.im[self.ndx].align,],
                      [tool.ClientData,], self.ndx)
        except AttributeError:
            pass

    def ColorWhite(self,*evnt):
        curim = self.im[self.ndx]
        self.listener(curim,['fontcolor',],[curim.fontcolor,],
            wx.Color(255,255,255))

    def ColorBlack(self, *evnt):
        curim = self.im[self.ndx]
        self.listener(curim,['fontcolor',],[curim.fontcolor,],
            wx.Color(0,0,0))

    def ChangeColor(self, *evnt):
        color = ColorPicker(self)
        if(color.data):
            curim = self.im[self.ndx]
            self.listener(curim,['fontcolor',],[curim.fontcolor,],
                          [color.data.GetColour(),],self.ndx)

    def SetDefaults(self, *evnt):

        confirm = wx.MessageDialog(None, "Are you sure you want to set \n" +
            "the current settings as Default?","Confirmation", wx.YES_NO | wx.ICON_QUESTION)
        confirm.CenterOnParent(wx.BOTH)
        confirm.Destroy()

        if(confirm.ShowModal() == wx.ID_YES):
            try:
                handle = self.im[self.ndx]
                Configx.Creator().writeDefaults(handle)
                dlg = wx.MessageDialog(None,"Defaults Changed","Confirmation",
                            wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()

            except AttributeError:
                dlg = wx.MessageDialog(None, "No Settings Selected",
                    "Error", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()

    def initToolbar(self, *evnt):
    
        toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.SIMPLE_BORDER)
        toolbar.SetToolBitmapSize(size=(16,16))

        if(os.path.isfile(os.path.join('icons','load.png'))):
            iconpath = os.path.join('icons','load.png')
        else:
            iconpath = os.path.join(self.exedir,'icons','load.png')
        toolLoad = toolbar.AddLabelTool(wx.ID_ANY,'',wx.Bitmap(iconpath),
                shortHelp="Load Directory", longHelp="Select a folder containing images")
        self.Bind(wx.EVT_MENU,self.loadIms,toolLoad)

        if(os.path.isfile(os.path.join('icons','apply.png'))):
            iconpath = os.path.join('icons','apply.png')
        else:
            iconpath = os.path.join(self.exedir,'icons','apply.png')
        self.toolApply = toolbar.AddLabelTool(wx.ID_ANY,'',wx.Bitmap(iconpath),
                shortHelp="Commit Changes", longHelp="Write changes to all images and save")

        self.Bind(wx.EVT_MENU, self.ExportChanges, self.toolApply)
        toolbar.EnableTool(self.toolApply.GetId(),False)

        toolbar.AddSeparator()

        if(os.path.isfile(os.path.join('icons','undo.png'))):
            iconpath = os.path.join('icons','undo.png')
        else:
            iconpath = os.path.join(self.exedir,'icons','undo.png')

        self.toolUndo = toolbar.AddLabelTool(wx.ID_ANY,'',wx.Bitmap(iconpath),
                shortHelp="Undo", longHelp="Undo previous change")
        self.Bind(wx.EVT_MENU, self.UndoChange, self.toolUndo)
        toolbar.EnableTool(self.toolUndo.GetId(),False)

        if(os.path.isfile(os.path.join('icons','redo.png'))):
            iconpath = os.path.join('icons','redo.png')
        else:
            iconpath = os.path.join(self.exedir,'icons','redo.png')

        self.toolRedo = toolbar.AddLabelTool(wx.ID_ANY,'',wx.Bitmap(iconpath),
                shortHelp="Redo", longHelp="Redo last change")
        self.Bind(wx.EVT_MENU, self.RedoChange, self.toolRedo)
        toolbar.EnableTool(self.toolRedo.GetId(),False)

        toolbar.AddSeparator()

        if(os.path.isfile(os.path.join('icons','topleft.png'))):
            iconpath = os.path.join('icons','topleft.png')
        else:
            iconpath = os.path.join(self.exedir,'icons','topleft.png')

        self.tl = toolbar.AddRadioLabelTool(wx.ID_ANY,'',wx.Bitmap(iconpath),
                shortHelp="Top Left", longHelp="Align date to Top Left", clientData=(0,0))

        if(os.path.isfile(os.path.join('icons','topright.png'))):
            iconpath = os.path.join('icons','topright.png')
        else:
            iconpath = os.path.join(self.exedir, 'icons','topright.png')

        self.tr = toolbar.AddRadioLabelTool(wx.ID_ANY,'',wx.Bitmap(iconpath),
                shortHelp="Top Right", longHelp="Align date to Top Right", clientData=(1,0))

        if(os.path.isfile(os.path.join('icons','bottomright.png'))):
            iconpath = os.path.join('icons','bottomright.png')
        else:
            iconpath = os.path.join(self.exedir,'icons','bottomright.png')

        self.br = toolbar.AddRadioLabelTool(wx.ID_ANY,'',wx.Bitmap(iconpath),
                shortHelp="Bottom Right", longHelp="Align date to Bottom Right", clientData=(1,1))

        if(os.path.isfile(os.path.join('icons','bottomleft.png'))):
            iconpath = os.path.join('icons','bottomleft.png')
        else:
            iconpath = os.path.join(self.exedir,'icons','bottomleft.png')

        self.bl = toolbar.AddRadioLabelTool(wx.ID_ANY,'',wx.Bitmap(iconpath),
                shortHelp="Bottom Left", longHelp="Align date to Bottom Left", clientData=(0,1))

        self.Bind(wx.EVT_MENU, lambda event: self.UpdateAlignment(event, self.tl), self.tl)
        self.Bind(wx.EVT_MENU, lambda event: self.UpdateAlignment(event, self.tr), self.tr)
        self.Bind(wx.EVT_MENU, lambda event: self.UpdateAlignment(event, self.br), self.br)
        self.Bind(wx.EVT_MENU, lambda event: self.UpdateAlignment(event, self.bl), self.bl)

        toolbar.AddSeparator()

        if(os.path.isfile(os.path.join('icons','colors.png'))):
            iconpath = os.path.join('icons','colors.png')
        else:
            iconpath = os.path.join(self.exedir,'icons','colors.png')

        self.toolColor = toolbar.AddLabelTool(wx.ID_ANY,'',wx.Bitmap(iconpath),
                shortHelp="Font Color", longHelp="Select font color")
        self.Bind(wx.EVT_MENU, self.ChangeColor, self.toolColor)
        toolbar.EnableTool(self.toolColor.GetId(),False)

        if(os.path.isfile(os.path.join('icons','cal3.png'))):
            iconpath = os.path.join('icons','cal3.png')
        else:
            iconpath = os.path.join(self.exedir,'icons','cal3.png')

        self.toolCal = toolbar.AddLabelTool(wx.ID_ANY,'',wx.Bitmap(iconpath),
                shortHelp="Change Date", longHelp="Select a replacement date for the image")
        self.Bind(wx.EVT_MENU, self.GetDate, self.toolCal)
        toolbar.EnableTool(self.toolCal.GetId(),False)

        toolbar.AddSeparator()

        toolbar.AddControl(wx.StaticText(toolbar, -1, "Date Format: "))

        formatChoices = ['M/D/YYYY','MM/DD/YYYY','Mon Day, Year','Month Day, Year']

        self.format = wx.Choice(toolbar, -1, choices=formatChoices)
        self.Bind(wx.EVT_CHOICE, self.formatSelect, self.format)
        toolbar.AddControl(self.format)
        self.format.Disable()

        toolbar.AddSeparator()

        toolbar.Realize()

        vbox = wx.BoxSizer(wx.VERTICAL)
        toolbar2 = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.SIMPLE_BORDER)

        toolbar2.AddControl(wx.StaticText(toolbar2, -1, "Font:"))

        #e = wx.FontEnumerator()
        #e.EnumerateFacenames()
        #fontchoices = e.GetFacenames()
        self.systemFonts = FontFinder.FindFonts()
        fontchoices = self.systemFonts.keys()
        fontchoices.sort()

        self.font = wx.Choice(toolbar2, -1, choices=fontchoices)
        self.Bind(wx.EVT_CHOICE, self.fontSelect, self.font)
        toolbar2.AddControl(self.font)
        self.font.Disable()

        toolbar2.AddSeparator()

        toolbar2.AddControl(wx.StaticText(toolbar2, -1, "Size:"))
        self.size = wx.SpinCtrl(toolbar2, -1, '', size=(60,20))
        self.size.SetRange(1,100)
        self.Bind(wx.EVT_SPINCTRL, self.fontSizeSelect, self.size)
        self.size.Disable()

        toolbar2.AddControl(self.size)

        toolbar2.AddSeparator()

        toolbar2.AddControl(wx.StaticText(toolbar2,-1,"Offset:"))

        toolbar2.AddSeparator()

        toolbar2.AddControl(wx.StaticText(toolbar2,-1, "X"))
        self.offsetx = wx.SpinCtrl(toolbar2, -1, '',size=(50,20))
        self.Bind(wx.EVT_SPINCTRL, self.updateOffset, self.offsetx)
        toolbar2.AddControl(self.offsetx)
        self.offsetx.Disable()

        toolbar2.AddSeparator()

        toolbar2.AddControl(wx.StaticText(toolbar2, -1, "Y"))
        self.offsety = wx.SpinCtrl(toolbar2, -1, '',size=(50,20))
        self.Bind(wx.EVT_SPINCTRL, self.updateOffset, self.offsety)
        toolbar2.AddControl(self.offsety)
        self.offsety.Disable()

        toolbar2.AddSeparator()

        self.aa = wx.Button(toolbar2, -1, "Apply to All")
        toolbar2.AddControl(self.aa)
        self.Bind(wx.EVT_BUTTON, self.Propogate, self.aa)
        self.aa.Disable()

        toolbar2.Realize()

        vbox.Add(toolbar, 0, wx.EXPAND)
        vbox.Add(toolbar2, 0, wx.EXPAND)
        vbox.Add(self.panel,1, wx.EXPAND)
        self.SetSizer(vbox)

        self.toolbar = toolbar
        self.toolbar2 = toolbar2

    def formatSelect(self, *evnt):

        curim = self.im[self.ndx]

        result = curim.SetDateFormat(self.format.GetSelection())
        self.listener(curim,['dateText','format'],
                     [curim.dateText,curim.format],
                     [result,self.format.GetSelection()],self.ndx)

    def Propogate(self, *evnt):

        applysettings.ApplyAll(self,APPLY_EVT_ID,self.im[self.ndx],self.im)

    def GetDate(self, *evnt):

        DatePicker(self.im[self.ndx], self.imbmp, self.format, self.listener, self.ndx)

    def onQuit(self, *evnt):
        """ Exit Confirmation """
        confirm = wx.MessageDialog(None, "Are you sure you want to exit?",
            "Confirmation", wx.YES_NO | wx.ICON_QUESTION)
        confirm.CenterOnParent(wx.BOTH)
        confirm.Destroy()

        if(confirm.ShowModal() == wx.ID_YES):
            self.Destroy()        
        
    def manageLayout(self):
      
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        crapbox = wx.StaticBoxSizer(self.box,wx.VERTICAL)
        crapbox.Add(self.imPanel, 1, wx.EXPAND | wx.ALL, 0)
        
        vbox1.Add(self.lbLabel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
        vbox1.Add(self.imList, 1, wx.EXPAND | wx.ALL,10)
        
        hbox1.Add(crapbox, 1, wx.EXPAND | wx.ALL,15)
        hbox1.Add(vbox1, 0, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 10)

        self.panel.SetSizer(hbox1)                
        
    def listClick(self, *evnt):
              
        self.ndx = self.imList.GetFocusedItem()
        self.im[self.ndx].Update(self.imbmp)
        self.updateControls(self.im[self.ndx])

    def updateControls(self, curim):

        # Update font controls
        self.font.SetStringSelection(curim.font.GetFaceName())

        # Update font size field
        self.size.SetValue(curim.fontsize)

        # Update offsets in x and y
        pos = self.im[self.ndx].position
        self.offsetx.SetValue(pos[0])
        self.offsety.SetValue(pos[1])

        # Update Alignment
        if(curim.align == (0,0)):
            self.toolbar.ToggleTool(self.tl.GetId(),1)
        elif(curim.align == (1,0)):
            self.toolbar.ToggleTool(self.tr.GetId(),1)
        elif(curim.align == (0,1)):
            self.toolbar.ToggleTool(self.bl.GetId(),1)
        else:
            self.toolbar.ToggleTool(self.br.GetId(),1)

        # Update Format:
        self.format.SetSelection(curim.format)
        
    def loadIms(self, *evnt):
    
        dirs = wx.DirDialog(self, "Please select Image folder")
        dirs.CenterOnParent()
                
        if(dirs.ShowModal() == wx.ID_OK):
            self.walkDirs(dirs.GetPath())
            self.SetStatusText("Loading Images...")
            
        dirs.Destroy()
        self.SetStatusText("Ready")
        
    def walkDirs(self, path):
    
        try:
            del self.im
        except:
            pass
    
        self.im = list()
        self.il.RemoveAll()
        self.imList.DeleteAllItems()

        ThreadedLoading.LoadIms(self,LOAD_EVT_ID,self.im,path,self.il,self.imList)

    def Enablers(self):

        self.format.Enable(True)
        self.size.Enable(True)
        self.font.Enable(True)
        self.offsetx.Enable(True)
        self.offsety.Enable(True)
        self.aa.Enable(True)

        self.menubar.commit.Enable(True)
        self.menubar.default.Enable(True)
        self.menubar.propogate.Enable(True)
        self.menubar.date.Enable(True)

        self.toolbar.EnableTool(self.toolCal.GetId(),True)
        self.toolbar.EnableTool(self.toolColor.GetId(),True)
        self.toolbar.EnableTool(self.toolApply.GetId(),True)

class App(wx.App):

    def OnInit(self):
        
        self.frame = Main(None, -1, "Date Stamper")

        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        #self.frame.Center(wx.BOTH)
        return True

if __name__ == "__main__":

    application = wx.PySimpleApp()

    if(os.path.isfile(os.path.join('icons','splash.png'))):
        impath = os.path.join('icons','splash.png')
    else:
        exedir = os.path.dirname(sys.executable)
        impath = os.path.join(exedir,'icons','splash.png')

    BM = wx.Image(impath,wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    AdvancedSplash.AdvancedSplash(None, bitmap=BM, timeout=3000)

    application.MainLoop()
    application.Destroy()

    LOAD_EVT_ID = wx.NewId()
    APPLY_EVT_ID = wx.NewId()
    COMMIT_EVT_ID = wx.NewId()
    app = App()
    app.MainLoop()