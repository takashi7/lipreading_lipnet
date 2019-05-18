import wx
import cv2
import numpy as np
from time import sleep

def create_wx_bitmap_from_cv2_image(cv2_image):
    height, width = cv2_image.shape[:2]
    return wx.BitmapFromBuffer(width, height, cv2_image)


class MyFrame(wx.Frame):
    def __init__(self, parent, title, fps=25):
        wx.Frame.__init__(self, parent, title=title)
        #wx.Panel.__init__(self, parent)
        
        video = np.load('video_face.npy')
        self.frame = video
        self.bmp = create_wx_bitmap_from_cv2_image(self.frame[0])
        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.i = 0
        self.Bind(wx.EVT_TIMER, self.NextFrame)


    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        if self.i < 75:
            self.bmp.CopyFromBuffer(self.frame[self.i-1])
            self.Refresh()
            print(self.i)
            self.i = self.i + 1
        else:
            self.i = 0
            self.timer.Stop()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "wxPython with OpenCV")
    frame.Show()
    app.MainLoop()       
        