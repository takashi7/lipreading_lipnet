import wx

class myFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        image = wx.Image('test.jpg')
        self.bitmap = image.ConvertToBitmap()

        wx.StaticBitmap(self, -1, self.bitmap, (0,0), self.GetClientSize())
        self.SetSize(image.GetSize())

app = wx.App(False)
frame = myFrame(None, "Image Viewer")
frame.Show()
app.MainLoop()