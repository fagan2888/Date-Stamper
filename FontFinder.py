import os
from PIL import ImageFont


def FindFonts():
    fontdir = 'C:\\Windows\\Fonts'

    files = os.listdir(fontdir)

    fonts = dict()

    for f in files:
        if (f.split('.')[1] == 'ttf'):
            tmp = ImageFont.truetype(os.path.join(fontdir,f),1)
            if(tmp.font.style == "Regular"):
                fonts[tmp.font.family]= f

    return fonts