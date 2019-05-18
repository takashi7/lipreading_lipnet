import wx
import cv2
import numpy as np
from time import sleep

def create_wx_bitmap_from_cv2_image(cv2_image):
    height, width = cv2_image.shape[:2]
    return wx.BitmapFromBuffer(width, height, cv2_image)

def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result

class MyFrame(wx.Frame):
    def __init__(self, parent, title, fps=25):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 500))
        self.fps = fps
        
        video = np.load('video_face.npy')
        self.frame = video
        self.bmp = create_wx_bitmap_from_cv2_image(self.frame[0])
        self.bmp = scale_bitmap(self.bmp, 400, 350)
        text = np.load('result_split.npy')
        self.subtitle = text
        self.inc = max(len(self.frame)/(len(self.subtitle)+1), 0.01)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.button1 = wx.Button(self, wx.ID_ANY, '1')
        self.button1.Bind(wx.EVT_BUTTON, self.click_button_start, self.button1)
        self.button2 = wx.Button(self, wx.ID_ANY, '2')
        self.button2.Bind(wx.EVT_BUTTON, self.click_button_stop, self.button2)
        self.button3 = wx.Button(self, wx.ID_ANY, '3')
        self.button3.Bind(wx.EVT_BUTTON, self.click_button_start, self.button3)

        self.layout = wx.BoxSizer(wx.HORIZONTAL)
        self.layout_button = wx.BoxSizer(wx.VERTICAL)
        self.layout_button.Add(self.button1, proportion=1)
        self.layout_button.Add(self.button2, proportion=1)
        self.layout_button.Add(self.button3, proportion=1)
        self.layout.Add(self.layout_button,flag=wx.EXPAND)
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
        dc.DrawBitmap(self.bmp, 300, 50)
        #self.main_frame = wx.StaticBitmap(self, wx.ID_ANY, self.bmp)

        self.layout_frame = wx.BoxSizer(wx.VERTICAL)
        #self.layout_frame.Add(self.main_frame)

        sub = " ".join(self.subtitle[:int(0/self.inc)])
        self.txt = wx.StaticText(self, -1, sub,(400,400))
        self.txt.SetBackgroundColour('#000000')

    def NextFrame(self, event):
        if self.i < 75:
            self.bmp = create_wx_bitmap_from_cv2_image(self.frame[self.i-1])
            self.bmp = scale_bitmap(self.bmp, 400, 350)
            #self.bmp.CopyFromBuffer(self.frame[self.i-1])
            sub = " ".join(self.subtitle[:int(self.i/self.inc)])
            
            self.txt = wx.StaticText(self, -1, sub,(400,500))
            #self.layout2.Add(self.txt, proportion=0, flag=wx.LEFT,  border=1000)
            self.layout_frame.Add(self.txt)
            self.layout.Add(self.layout_frame)
            print(sub)
            self.Refresh()
            print(self.i)
            self.i = self.i + 1
        else:
            self.i = 0
            self.layout.Remove(self.layout_frame)
            self.layout.Layout()
            self.Refresh()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "LipNet")
    frame.Show()
    app.MainLoop()       
        