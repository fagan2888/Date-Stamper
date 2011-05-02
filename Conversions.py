from PIL import Image
import wx

def piltoimage(pil,alpha=1):
    """Convert PIL Image to wx.Image."""

    if alpha:
        image = apply( wx.EmptyImage, pil.size )
        image.SetData( pil.convert( "RGB").tostring() )
    else:
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        new_image = pil.convert('RGB')
        data = new_image.tostring()
        image = wx.BitmapFromImage(data)
    return image

def imagetopil(self,image):
    """Convert wx.Image to PIL Image."""
    pil = Image.new('RGB', (image.GetWidth(), image.GetHeight()))
    pil.fromstring(image.GetData())
    
    return pil

def padpiltoimage(pil,width,height,alpha=True):
    """Convert PIL Image to wx.Image."""
    output = Image.new("RGBA", (width,height))
    output.paste(pil, ((width - pil.size[0])/2,
                       (height - pil.size[1])/2))

    if alpha:
        image = apply( wx.EmptyImage, (output.size[0], output.size[1]) )
        image.SetData( output.convert( "RGB").tostring() )
        image.SetAlphaData(output.convert("RGBA").tostring()[3::4])
    else:
        image = wx.EmptyImage(output.size[0], output.size[1])
        new_image = output.convert('RGB')
        data = new_image.tostring()
        image.SetData(data)
    return image