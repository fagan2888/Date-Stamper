""" This Module will handle all importing and exporting of configurations """

import wx

class Creator:

    def __init__(self):

        self.config = wx.Config('Date Stamper','Jonathan Suever')

        #self.config.Write('Creator','Jonathan Suever')
        #self.config.Flush()


    def writeDefaults(self, handle):

        self.config.WriteInt('format',handle.format)
        self.config.WriteInt('fontsize',handle.fontsize)

        r,g,b = handle.fontcolor.Get()

        self.config.WriteInt('red',r)
        self.config.WriteInt('green',g)
        self.config.WriteInt('blue',b)

        self.config.WriteInt('alignx',handle.align[0])
        self.config.WriteInt('aligny',handle.align[1])

        self.config.Write('fontfamily',handle.fontfamily)

        self.config.WriteInt('posx',handle.position[0])
        self.config.WriteInt('posy',handle.position[1])

        self.config.Flush()

    def readDefaults(self):

        result = dict()

        result['format'] = self.config.ReadInt('format', defaultVal=0)
        result['fontsize'] = self.config.ReadInt('fontsize', defaultVal=7)
        result['fontfamily'] = self.config.Read('fontfamily', defaultVal='Arial')
        result['align'] = self.config.ReadInt('alignx', defaultVal=1),self.config.ReadInt('aligny', defaultVal=1)
        result['offsets'] = self.config.ReadInt('posx', defaultVal=3),self.config.ReadInt('posy', defaultVal=3)
        result['color'] = [self.config.ReadInt('red', defaultVal=255),
                           self.config.ReadInt('green', defaultVal=255),
                           self.config.ReadInt('blue', defaultVal=255)]

        return result

def export(exportDict):
    """ Takes the Fields supplied as a dictionary and puts them into the config """

    if(exists):
        pass
    else:
        pass
        

def importConfig(Field):
    """ This retrieves information from the configuration file """
    pass