
import wx
import GetHelp

def Create(self):

    menubar = wx.MenuBar()

    file = wx.Menu()
    open = wx.MenuItem(file, -1, "&Open Directory\tCtrl+O")
    menubar.commit = wx.MenuItem(file, -1, "&Commit Changes\tCtrl+S")
    quit = wx.MenuItem(file, -1, '&Exit\tCtrl+W')

    file.AppendItem(open)
    file.AppendItem(menubar.commit)
    file.AppendSeparator()
    file.AppendItem(quit)

    edit = wx.Menu()
    menubar.undo = wx.MenuItem(edit, -1, "&Undo\tCtrl+Z")
    menubar.redo = wx.MenuItem(edit, -1, "&Redo\tCtrl+Shift+Z")
    edit.AppendItem(menubar.undo)
    edit.AppendItem(menubar.redo)
    edit.AppendSeparator()

    menubar.date = wx.MenuItem(edit, -1, "Change Date")
    edit.AppendItem(menubar.date)
    edit.AppendSeparator()
    menubar.propogate = wx.MenuItem(edit, -1, "Propogate Current")
    edit.AppendItem(menubar.propogate)
    menubar.default = wx.MenuItem(edit, -1, "Set As Default")
    edit.AppendItem(menubar.default)


    help = wx.Menu()
    about = wx.MenuItem(help, -1, "About Date Stamper")
    proghelp = wx.MenuItem(help, -1, "Help")
    help.AppendItem(about)
    help.AppendSeparator()
    help.AppendItem(proghelp)

    menubar.Append(file, "&File")
    menubar.Append(edit, "&Edit")
    menubar.Append(help, "&Help")

    self.SetMenuBar(menubar)
    self.Bind(wx.EVT_MENU, self.loadIms, id=open.GetId())
    self.Bind(wx.EVT_MENU, self.onQuit, id=quit.GetId())
    self.Bind(wx.EVT_MENU, self.about, id=about.GetId())
    self.Bind(wx.EVT_MENU, self.ExportChanges, id=menubar.commit.GetId())
    self.Bind(wx.EVT_MENU, self.SetDefaults, id=menubar.default.GetId())
    self.Bind(wx.EVT_MENU, GetHelp.DispHelp, id=proghelp.GetId())
    self.Bind(wx.EVT_MENU, self.UndoChange, id=menubar.undo.GetId())
    self.Bind(wx.EVT_MENU, self.RedoChange, id=menubar.redo.GetId())
    self.Bind(wx.EVT_MENU, self.GetDate, id=menubar.date.GetId())
    self.Bind(wx.EVT_MENU, self.Propogate, id=menubar.propogate.GetId())

    # Disable the correct buttons
    menubar.commit.Enable(False)
    menubar.undo.Enable(False)
    menubar.redo.Enable(False)
    menubar.date.Enable(False)
    menubar.default.Enable(False)
    menubar.propogate.Enable(False)

    return menubar