import wx
import cv2
import numpy as np
from time import sleep

def create_wx_bitmap_from_cv2_image(cv2_image):
    height, width = cv2_image.shape[:2]
    return wx.BitmapFromBuffer(width, height, cv2_image)


class MyFrame(wx.Frame):
    def __init__(self, parent, title, fps=25):
        wx.Frame.__init__(self, parent, title=title, size=(360, 318))
        self.fps = fps
        
        video = np.load('video_face.npy')
        self.frame = video
        self.bmp = create_wx_bitmap_from_cv2_image(self.frame[0])
        text = np.load('result_split.npy')
        self.subtitle = text
        self.inc = max(len(self.frame)/(len(self.subtitle)+1), 0.01)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.start_button = wx.Button(self, wx.ID_ANY, 'Start')
        self.start_button.Bind(wx.EVT_BUTTON, self.click_button_start, self.start_button)
        self.stop_button = wx.Button(self, wx.ID_ANY, 'Stop')
        self.stop_button.Bind(wx.EVT_BUTTON, self.click_button_stop, self.stop_button)
        self.layout = wx.BoxSizer(wx.HORIZONTAL)
        self.layout.Add(self.start_button)
        self.layout.Add(self.stop_button)
        self.SetSizer(self.layout)

    
    def click_button_start(self, e):
        self.timer = wx.Timer(self)
        self.timer.Start(1000./self.fps)        
        self.i = 0
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def click_button_stop(self, e):      
        self.timer.Stop()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 30)
        sub = " ".join(self.subtitle[:int(0/self.inc)])
        self.txt = wx.StaticText(self, -1, sub,(40,40))

    def NextFrame(self, event):
        if self.i < 75:
            self.bmp.CopyFromBuffer(self.frame[self.i-1])
            sub = " ".join(self.subtitle[:int(self.i/self.inc)])

            self.txt.SetLabel(sub)
            print(sub)
            #txt = wx.StaticText(self, -1, sub,(40,40))
            self.Refresh()
            print(self.i)
            self.i = self.i + 1
        else:
            self.i = 0
            self.Refresh()
            #self.txt.Hide()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "LipNet")
    frame.Show()
    app.MainLoop()       
        